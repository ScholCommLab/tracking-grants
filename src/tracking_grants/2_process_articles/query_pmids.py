# -*- coding: utf-8 -*-
import asyncio
import csv
import re
from datetime import datetime

import aiofiles
import aiohttp
import pandas as pd
from throttler import Throttler
from tqdm.auto import tqdm
from tracking_grants import articles_f, email, ncbi_api_key, pmid_f, tool_name
from tracking_grants.utils.logging import logger

COUNT_REGEX = r"<Count>(\d+)<\/Count>"
ID_REGEX = r"<Id>(\d+)<\/Id>"


class Eutils:
    """Asynchronous API client to retrieve PMIDs for DOIs."""

    def __init__(self, tool, email, api_key):
        self.baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.tasks = None

        self.tool = tool
        self.email = email
        self.api_key = api_key

        self.throttler = Throttler(rate_limit=10, period=1)

    async def __fetch(self, session, params):
        try:
            async with self.throttler:
                ts = datetime.now().isoformat()
                await asyncio.sleep(0.1)
                async with session.get(self.baseurl, params=params) as resp:
                    text = await resp.text()
                    return ts, text
        except aiohttp.ClientError as e:
            logger.error(
                "aiohttp exception for %s [%s]: %s",
                params['term'],
                getattr(e, "status", None),
                getattr(e, "message", None),
            )
            return ts, str(e)

    async def __parse(self, session, doi):
        pmid = None
        ts = None
        text = None

        params = {
            "tool": self.tool,
            "email": self.email,
            "api_key": self.api_key,
            "db": "pubmed",
            "retmax": 1,
            "term": doi,
        }

        try:
            ts, text = await self.__fetch(session, params)
        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:
            logger.error(
                "aiohttp exception for %s [%s]: %s",
                doi,
                getattr(e, "status", None),
                getattr(e, "message", None),
            )
            return None, None, None
        else:
            if "PhraseNotFound" not in text:
                count = re.search(COUNT_REGEX, text)
                if count:
                    count = int(count.group(1))
                    # Only return unique matches
                    if count == 1:
                        match = re.search(ID_REGEX, text)
                        if match:
                            pmid = match.group(1)
        return pmid, ts, text

    async def get_pmid(self, session, doi, writer):
        pmid, ts, text = await self.__parse(session, doi)
        writer.writerow([doi, pmid, text, ts])

    async def run(self, dois, writer):
        connector = aiohttp.TCPConnector(limit=1)
        timeout = aiohttp.ClientTimeout(total=1.1 * 4 * len(dois) / 10)
        async with aiohttp.ClientSession(
            connector=connector, timeout=timeout
        ) as session:
            # Create tasks with DOI
            tasks = []
            for doi in dois:
                t = asyncio.ensure_future(self.get_pmid(session, doi, writer))
                tasks.append(t)

            # Await tasks and print progress for responses
            for t in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                await t


def query_pmids(articles_f, pmid_f):
    articles = pd.read_csv(articles_f)

    if not pmid_f.exists():
        with pmid_f.open("w") as f:
            fieldnames = ["DOI", "pmid", "response", "ts"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    pmids = pd.read_csv(pmid_f)
    existing_dois = set(pmids.DOI.tolist())

    dois = articles.DOI.unique().tolist()
    dois = list(set(dois).difference(existing_dois))

    if len(dois) == 0:
        logger.info("\tAll DOIs have been queried already.")
        return None
    else:
        logger.info("\tEnriching articles with Pubmed IDs.")
        eutils = Eutils(tool_name, email, ncbi_api_key)

        with pmid_f.open("a") as f:
            writer = csv.writer(f)

            loop = asyncio.get_event_loop()
            loop.run_until_complete(eutils.run(dois, writer))


def process_pmids(articles_f, pmid_f):
    articles = pd.read_csv(articles_f)
    articles["pmid"] = None

    pmids = pd.read_csv(pmid_f)

    articles = articles.merge(
        pmids[["DOI", "pmid"]], left_on="DOI", right_on="DOI", how="left"
    )
    articles.to_csv(articles_f, index=False)


def run():
    articles = pd.read_csv(articles_f, nrows=5)
    if "pmid" not in articles.columns:
        query_pmids(articles_f, pmid_f)
        logger.info("\tProcessing the NCBI responses and merging PMIDs.")
        process_pmids(articles_f, pmid_f)
    else:
        logger.info("\tSkipped: Dataset already contains pmid columns.")
