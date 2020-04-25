# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET

import pandas as pd
import requests
from tqdm.auto import tqdm

from military_grants import articles_f
from military_grants.utils.logging import logger


class Eutils:
    def __init__(self, tool, email, api_key):
        self.search_api = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.params = {
            "tool": tool,
            "email": email,
            "api_key": api_key,
            "db": "pubmed",
            "retmax": 1,
        }

    def search(self, doi):
        params = self.params
        params["term"] = doi
        return requests.get(self.search_api, params=params)


def query_pmids(articles_f):
    articles = pd.read_csv(articles_f, index_col="article_id")

    tool = os.getenv("NCBI_TOOL")
    email = os.getenv("NCBI_EMAIL")
    api_key = os.getenv("NCBI_API_KEY")

    eutils = Eutils(tool, email, api_key)

    for ix, row in tqdm(articles.iterrows(), total=len(articles)):
        try:
            resp = eutils.search(row["DOI"])
        except Exception as e:
            print(e)

        root = ET.fromstring(resp.text)
        pmids = root.findall("*/Id")
        if pmids:
            articles.loc[ix, "pmid"] = pmids[0].text

    articles.to_csv(articles_f)


def run():
    articles = pd.read_csv(articles_f, index_col="article_id")

    if "pmid" not in articles.columns:
        logger.info("Enriching articles with Pubmed IDs.")
        query_pmids(articles_f)
    else:
        logger.info("Dataset already contains pmid columns.")
