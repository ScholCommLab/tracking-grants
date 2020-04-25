# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

from military_grants import data_dir
from military_grants import input_folder, references_f
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
    pubs.index.name = "reference_id"
    pubs.columns = ["grant_id", "reference", "type"]

    # Write unique references to files
    logger.debug("Writing cleaned publication data to CSV")
    pubs.to_csv(input_f)


def run():
    excel_files = input_folder.glob("*.xlsx")

    if not Path(references_f).exists():
        logger.info("Merge excel spreadsheets and export to CSV")
        process_excel(excel_files, references_f)
    else:
        logger.info("Skipping: Excel files has already been processed")
