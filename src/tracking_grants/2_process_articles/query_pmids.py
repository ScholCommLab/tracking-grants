# -*- coding: utf-8 -*-
import asyncio
import re

import aiohttp
import pandas as pd
from asyncio_throttle import Throttler
from tqdm.auto import tqdm
from tracking_grants import articles_f, pmid_f, email, ncbi_api_key, tool_name
from tracking_grants.utils.logging import logger


COUNT_REGEX = r"<Count>(\d+)<\/Count>"
ID_REGEX = r"<Id>(\d+)<\/Id>"


class Eutils:
    """Asynchronous API client to retrieve PMIDs for DOIs."""

    def __init__(self, tool, email, api_key, loop, calls_per_sec=3):
        self.baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.params = {
            "tool": tool,
            "email": email,
            "api_key": api_key,
            "db": "pubmed",
            "retmax": 1,
        }
        self.loop = loop
        self.throttler = Throttler(rate_limit=calls_per_sec, period=1)

    async def __fetch(self, session, params):
        async with self.throttler:
            async with session.get(self.baseurl, params=params) as resp:
                await asyncio.sleep(1)
                return await resp.text()

    async def __parse(self, text):
        pmid = None
        if "PhraseNotFound" not in text:
            count = re.search(COUNT_REGEX, text)
            if count:
                count = int(count.group(1))
                # Only return unique matches
                if count == 1:
                    match = re.search(ID_REGEX, text)
                    if match:
                        pmid = match.group(1)
        return pmid

    async def get_pmid(self, session, doi):
        params = self.params
        params["term"] = doi

        text = await self.__fetch(session, params)
        pmid = await self.__parse(text)
        return (doi, pmid)

    async def run(self, dois):
        tasks = []
        async with aiohttp.ClientSession(loop=self.loop) as session:
            # Create tasks with DOI
            tasks = [asyncio.ensure_future(self.get_pmid(session, doi)) for doi in dois]

            # Await tasks and print progress
            responses = [
                await t for t in tqdm(asyncio.as_completed(tasks), total=len(dois))
            ]

            return responses


def query_pmids(articles_f, pmid_f):
    articles = pd.read_csv(articles_f)
    dois = articles.DOI.unique().tolist()

    # Init search with user data
    loop = asyncio.get_event_loop()
    eutils = Eutils(tool_name, email, ncbi_api_key, loop)
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(eutils.run(dois))
    finally:
        loop.close()
        asyncio.set_event_loop(None)

    pd.DataFrame(results, columns=["DOI", "pmid"]).to_csv(pmid_f)


def process_pmids(articles_f, pmid_f):
    articles = pd.read_csv(articles_f)
    articles["pmid"] = None

    pmids = pd.read_csv(pmid_f)

    articles = articles.merge(pmids, left_on="DOI", right_on="DOI", how="left")
    articles.to_csv(articles_f, index=False)


def run():
    articles = pd.read_csv(articles_f, nrows=5)

    if "pmid" not in articles.columns:
        if not pmid_f.exists():
            logger.info("\tEnriching articles with Pubmed IDs.")
            query_pmids(articles_f, pmid_f)

        process_pmids(articles_f, pmid_f)
    else:
        logger.info("\tSkipped: Dataset already contains pmid columns.")
