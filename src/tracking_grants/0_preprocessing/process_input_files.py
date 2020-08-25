# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path

from tracking_grants import input_folder, references_f, awards_f
from tracking_grants.utils.logging import logger


def clean_reference(ref):
    ref = ref.lstrip("·")
    ref = ref.replace("\n", " ")
    ref = " ".join(ref.split())
    return ref


def process_publications(input_files: list, output_f: Path):
    """ Runs some preprocessing on input Excel in "data/external" to
    de-duplicate exports it into two formats:
        1. CSV for further processing
        2. Text file with one citation per line for citation parsing
    """
    logger.debug("Load publication spreadsheets and run some preprocessing.")

    # Load excel files
    dfs = []
    for f in input_files:
        df = pd.read_csv(f, index_col=0)
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
    pubs.to_csv(output_f)


def process_awards(input_files, output_f):
    logger.debug("Load awards spreadsheets and run some preprocessing.")

    # Load excel files
    dfs = []
    for f in input_files:
        df = pd.read_csv(f)
        dfs.append(df)

    # Merge datasets
    awards = pd.concat(dfs)

    print(awards.columns)

    # Drop duplicate entries
    logger.debug(f"Duplicate entries in dataset: {sum(awards.duplicated())}")
    awards = awards.drop_duplicates()

    # Reindex and rename columns
    awards.index = range(0, len(awards))
    awards.index.name = "award_id"

    # Write unique references to files
    logger.debug("Writing cleaned award data to CSV")
    awards.to_csv(output_f)


def run():
    publications = input_folder.glob(f"publications/*.csv")
    awards = input_folder.glob(f"awards/*.csv")

    if not Path(references_f).exists():
        logger.info("\tMerge publication spreadsheets and export to CSV")
        process_publications(publications, references_f)
    else:
        logger.info("\tSkipped: Publications have already been processed")

    if not Path(awards_f).exists():
        logger.info("\tMerge awards spreadsheets and export to CSV")
        process_awards(awards, awards_f)
    else:
        logger.info("\tSkipped: Awards have already been processed")
