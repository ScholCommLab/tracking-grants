# -*- coding: utf-8 -*-
import re

import pandas as pd
import requests
from ratelimit import limits, sleep_and_retry
from tqdm.auto import tqdm
from tracking_grants import articles_f, email, ncbi_api_key, tool_name
from tracking_grants.utils.logging import logger


tqdm.pandas()


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
    
    @sleep_and_retry
    @limits(calls=10, period=1)
    def search(self, doi):
        params = self.params
        params["term"] = doi
        
        r = requests.get(self.search_api, params=params)
        
        # Only return DOI has been found in the text
        if 'PhraseNotFound' not in r.text:
            count = int(re.search(r"<Count>(\d+)<\/Count>", r.text).group(1))
            # Only return unique matches
            if count == 1:
                match = re.search(r"<Id>(\d+)<\/Id>", r.text)
                if match:
                    return match.group(1)
        return None


def query_pmids(articles_f):
    articles = pd.read_csv(articles_f)

    # Init search with user data
    eutils = Eutils(tool_name, email, ncbi_api_key)

    # Query PMIDs with DOIs
    articles['pmid'] = articles.DOI.progress_map(eutils.search)
    articles.to_csv(articles_f, index=False)


def run():
    articles = pd.read_csv(articles_f, nrows=5)

    if "pmid" not in articles.columns:
        logger.info("\tEnriching articles with Pubmed IDs.")
        query_pmids(articles_f)
    else:
        logger.info("\tSkipped: Dataset already contains pmid columns.")
