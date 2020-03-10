# -*- coding: utf-8 -*-
from pathlib import Path

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm

from src.utils.apis import CrossrefAPI
from src.utils.mylogger import logger


def query_crossref(pubs):
    """ Queries Crossref API with bibliographic queries to retrieve one result per citation
    """
    # Initialise Crossref API endpoint
    crossref = CrossrefAPI()

    # Queries
    results = {}
    status_codes = {}

    df = pubs.sample(200).copy()
    for ix, row in tqdm(df.iterrows(), total=len(df), desc="Crossref API"):
        r = crossref.query(row.unstruct_citation)
        status_codes[ix] = r.status_code
        if r.status_code == 200:
            results[ix] = r.json()["message"]["items"][0]

    cr_results = pd.DataFrame.from_dict(results).T
    cr_results.index.name = "article_id"

    return cr_results


def main():
    """ Query for additional identifiers.
        Always queries Crossref with bibliometric queries.
        Optionally, queries NCBI for PMIDs and PMCIDs
    """
    # Load dataset
    pubs = pd.read_csv(articles, index_col="article_id")

    logger.info("Querying Crossref")
    cr_results = query_crossref(pubs)

    logger.info(f"Writing Crossref results to `{crossref_outfile}`")
    cr_results.to_csv(crossref_outfile)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    articles = data_dir / "interim/structured.csv"
    crossref_outfile = data_dir / "interim/_crossref.csv"
    articles_with_dois = data_dir / "interim/queried_ids.csv"

    load_dotenv(find_dotenv())

    main()
