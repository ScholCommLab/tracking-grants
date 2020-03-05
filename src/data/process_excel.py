# -*- coding: utf-8 -*-
from pathlib import Path

import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm

from src.utils.mylogger import logger


def process_excel():
    """ Runs some preprocessing on input Excel in "data/external" to
    de-duplicate exports it into two formats:
        1. CSV for further processing
        2. Text file with one citation per line for citation parsing
    """
    logger.info("Load Excel spreadsheet and run some preprocessing.")
    input_file = data_dir / "external/Awards_Pubs_CDMRP212020.xls"

    # Load excel file
    pt_pubs = pd.read_excel(input_file, sheet_name=1, index_col=0)
    bc_pubs = pd.read_excel(input_file, sheet_name=3, index_col=0)

    # Merge datasets
    pt_pubs["type"] = "PH_TBI"
    bc_pubs["type"] = "BC"
    pubs = pd.concat([pt_pubs, bc_pubs])

    # Drop duplicate entries
    logger.info(f"Duplicate entries in dataset: {sum(pubs.duplicated())}")
    pubs = pubs.drop_duplicates()

    # Reindex and rename columns
    pubs.index = range(0, len(pubs))
    pubs.index.name = "article_id"
    pubs.columns = ["proposal_id", "unstruct_citation", "type"]

    # Write unique references to files
    logger.info("Writing cleaned publication data to CSV")
    pubs.to_csv(data_dir / "interim/input.csv")

    # Write references into text files for `anystyle`
    logger.info("Writing unstructured references to txt")
    with open(str(data_dir / "interim/_unstructured_references.txt"), "w") as f:
        for l in pubs['unstruct_citation']:
            f.write(l + "\n")


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    process_excel()
