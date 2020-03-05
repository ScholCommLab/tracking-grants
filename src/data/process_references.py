# -*- coding: utf-8 -*-
from pathlib import Path

import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm

from src.utils.mylogger import logger

import json
import numpy as np

import pandas as pd


def process_unstruct_refs(df):
    """ Processes JSON output from `anystyle`.

    1. Fixes DOI by removing unwanted trailing characters
    2. Constructs author strings from anystyle output
    3. Convert dates to years
    4. Return selection of columns

    """
    # Fix DOIs (remove trailing periods)
    df["DOI"] = df["DOI"].map(
        lambda x: (x[:-1] if x[-1] in [".", ";", ":"] else x)
        if not pd.isna(x)
        else np.nan
    )

    # Process author name strings
    for ix, r in df.iterrows():
        names = r["author"]
        name_str = ""

        if type(names) == list:
            if "literal" in names[0]:
                name_str = names[0]["literal"]
            else:
                for pos, n in enumerate(names):
                    if "family" in n:
                        name_str = name_str + n["family"]
                    if "given" in n:
                        name_str = name_str + ", " + n["given"]
                    if pos < len(names) - 1:
                        name_str = name_str + "; "

            df.loc[ix, "author_str"] = name_str

    # Process date
    for ix, r in df.iterrows():
        date = r["issued"]
        year = None

        if pd.notna(date):
            year = date[0:4]
            if year.isdigit():
                df.loc[ix, "year"] = int(year)
            else:
                df.loc[ix, "year"] = None

    return df[
        [
            "DOI",
            "PMCID",
            "PMID",
            "URL",
            "year",
            "container-title",
            "title",
            "author_str",
        ]
    ]


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    # Load datasets
    pubs = pd.read_csv(data_dir / "interim/input.csv", index_col="article_id")

    logger.info("Load parsed reference information from JSON")
    df = pd.read_json(
        open(str(data_dir / "interim/_structured_references.json"), "r"),
        dtype={"PMCID": object, "PMID": object},
    )

    logger.info("Processing the data")
    parsed = process_unstruct_refs(df)

    logger.info("Merge with data from granting agency")
    pubs = pubs.join(parsed)

    logger.info("Write output")
    pubs.to_csv(data_dir / "interim/structured.csv")
