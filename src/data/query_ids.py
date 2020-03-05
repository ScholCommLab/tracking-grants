# -*- coding: utf-8 -*-
from pathlib import Path

import click
import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm

from src.utils.apis import *
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
    cr_results.to_csv(data_dir / "interim/_crossref_responses.csv")

    return cr_results


def match_dois(pubs, cr_results, cr_score):
    """ Accept Crossref match if score is higher than 80 (or as defined in function params)
    """
    for ix, row in cr_results.iterrows():
        pubs.loc[ix, "CR_DOI_candidate"] = row["DOI"]
        pubs.loc[ix, "CR_DOI_score"] = row["score"]
        # if row["score"] > cr_score:
        #     pubs.loc[ix, "CR_DOI"] = row["DOI"]
        # else:
        #     pubs.loc[ix, "CR_DOI"] = None


def query_ncbi(cr_results):
    """ Queries NCBI API with up to 200 DOIs per request and tries to retrieve PMIDs/PMCIDs
    """
    # Initialise NCBI API
    ncbi = NCBIAPI()

    total = len(cr_results)
    ids_per_req = 200

    items = []
    for ix in tqdm(range(0, total, ids_per_req), total=(total // ids_per_req) + 1,):
        imin = ix
        if imin + ids_per_req < total:
            imax = imin + ids_per_req
        else:
            imax = total

        dois = cr_results.iloc[imin:imax]["DOI"].dropna().tolist()
        r = ncbi.query(dois)

        if r.status_code == 200:
            print(len(r.json()["records"]))
            items.extend(r.json()["records"])
        else:
            print(r.status_code)
            break


@click.command()
@click.option("--ncbi", is_flag=True, help="Run NCBI queries as well")
@click.option("--cr_score", default=80, help="Minimum score for Crossref matches")
def main(ncbi, cr_score):
    """ Query for additional identifiers.
        Always queries Crossref with bibliometric queries.
        Optionally, queries NCBI for PMIDs and PMCIDs
    """
    # Load dataset
    pubs = pd.read_csv(data_dir / "interim/structured.csv", index_col="article_id")

    logger.info("Querying Crossref")
    cr_results = query_crossref(pubs)

    logger.info("Matching DOIs")
    match_dois(pubs, cr_results, cr_score)

    if ncbi:
        query_ncbi(cr_results)

    logger.info("Writing articles with matched IDs")
    pubs.to_csv(data_dir / "interim/queried_ids.csv")


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    load_dotenv(find_dotenv())

    main()
