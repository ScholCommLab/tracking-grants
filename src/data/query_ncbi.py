# -*- coding: utf-8 -*-
from pathlib import Path

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm

from src.utils.apis import NCBIAPI
from src.utils.mylogger import logger


def query_ncbi(metadata):
    """

    """
    # Initialise NCBI API
    ncbi = NCBIAPI()

    results = {}
    dois = metadata.DOI.dropna().iloc[0:10]
    for ix, doi in tqdm(dois.iteritems(), total=len(dois)):
        r = ncbi.query(doi)

        if r.json()['status'] == "ok":
            results[ix] = r.json()["records"][0]
        else:
            results[ix] = None

    df = pd.DataFrame.from_dict(results).T
    df.index.name = "article_id"

    df.to_csv(ncbi_file)
    return results


def main():
    """ Query for additional identifiers.
        Always queries Crossref with bibliometric queries.
        Optionally, queries NCBI for PMIDs and PMCIDs
    """
    # Load dataset
    metadata = pd.read_csv(metadata_file, index_col="article_id")

    logger.info("Querying Crossref")
    results = query_ncbi(metadata)

    metadata['pmid'] = None
    metadata['pmcid'] = None

    for ix, r in results.items():
        if r:
            for ncbi_id in ['pmid', 'pmcid']:
                if ncbi_id in r:
                    metadata.loc[ix, ncbi_id] = r[ncbi_id]

    logger.info(f"Writing NCBI results to `{metadata_}`")
    metadata.to_csv(metadata_)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    ncbi_file = data_dir / "interim/_ncbi.csv"
    metadata_file = data_dir / "processed/article_metadata.csv"
    metadata_ = data_dir / "processed/metadata_.csv"

    load_dotenv(find_dotenv())

    main()
