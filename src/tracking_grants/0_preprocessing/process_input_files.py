# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

from tracking_grants import input_folder, references_f
from tracking_grants.utils.logging import logger


def clean_reference(ref):
    ref = ref.lstrip("·")
    ref = ref.replace("\n", " ")
    ref = " ".join(ref.split())
    return ref


def process_excel(input_files: list, input_f: Path, file_format: str):
    """ Runs some preprocessing on input Excel in "data/external" to
    de-duplicate exports it into two formats:
        1. CSV for further processing
        2. Text file with one citation per line for citation parsing
    """
    logger.debug("Load Excel spreadsheet and run some preprocessing.")

    # Load excel files
    dfs = []
    for f in input_files:
        if file_format == "csv":
            df = pd.read_csv(f, index_col=0)
        else:
            df = pd.read_excel(f, index_col=0)
        df["program"] = f.name.split(".")[0]
        dfs.append(df)

    # Merge datasets
    pubs = pd.concat(dfs)

    # Drop duplicate entries
    logger.debug(f"Duplicate entries in dataset: {sum(pubs.duplicated())}")
    pubs = pubs.drop_duplicates()

    # Reindex and rename columns
    pubs.index = range(0, len(pubs))
    pubs.index.name = "reference_id"
    pubs.columns = ["grant_id", "reference", "program"]

    pubs['reference'] = pubs['reference'].map(clean_reference)

    # Write unique references to files
    logger.debug("Writing cleaned publication data to CSV")
    pubs.to_csv(input_f)


def run():
    file_format = "csv"
    input_files = input_folder.glob(f"*.{file_format}")

    if not Path(references_f).exists():
        logger.info("\tMerge excel spreadsheets and export to CSV")
        process_excel(input_files, references_f, file_format)
    else:
        logger.info("\tSkipped: Excel files has already been processed")
