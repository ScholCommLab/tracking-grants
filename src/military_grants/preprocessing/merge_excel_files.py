# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

from military_grants import data_dir
from military_grants import EXCEL, REFERENCES
from military_grants.utils.logging import logger


def process_excel(excel_files: list, input_f: Path):
    """ Runs some preprocessing on input Excel in "data/external" to
    de-duplicate exports it into two formats:
        1. CSV for further processing
        2. Text file with one citation per line for citation parsing
    """
    logger.debug("Load Excel spreadsheet and run some preprocessing.")

    # Load excel files
    dfs = []
    for f in excel_files:
        df = pd.read_excel(f, index_col=0)
        df["type"] = f.name.split(".")[0]
        dfs.append(df)

    # Merge datasets
    pubs = pd.concat(dfs)

    # Drop duplicate entries
    logger.debug(f"Duplicate entries in dataset: {sum(pubs.duplicated())}")
    pubs = pubs.drop_duplicates()

    # Reindex and rename columns
    pubs.index = range(0, len(pubs))
    pubs.index.name = "article_id"
    pubs.columns = ["proposal_id", "unstruct_citation", "type"]

    # Write unique references to files
    logger.debug("Writing cleaned publication data to CSV")
    pubs.to_csv(input_f)


def run():
    input_folder = data_dir / EXCEL
    excel_files = input_folder.glob("*.xlsx")

    references_f = data_dir / REFERENCES

    if not Path(references_f).exists():
        logger.info("Process Excel file")
        process_excel(excel_files, references_f)
    else:
        logger.info("Skipping: Excel file has already been processed")
