# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from military_grants.utils.logging import logger


def process_excel(excel_f, input_f):
    """ Runs some preprocessing on input Excel in "data/external" to
    de-duplicate exports it into two formats:
        1. CSV for further processing
        2. Text file with one citation per line for citation parsing
    """
    logger.debug("Load Excel spreadsheet and run some preprocessing.")

    # Load excel file
    pt_pubs = pd.read_excel(excel_f, sheet_name=1, index_col=0)
    bc_pubs = pd.read_excel(excel_f, sheet_name=3, index_col=0)

    # Merge datasets
    pt_pubs["type"] = "PH_TBI"
    bc_pubs["type"] = "BC"
    pubs = pd.concat([pt_pubs, bc_pubs])

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


def process_input(input_f, unstructured_refs_f):
    pubs = pd.read_csv(input_f)

    # Write references into text files for `anystyle`
    logger.debug("Writing unstructured references to txt")
    with open(unstructured_refs_f, "w") as f:
        for l in pubs["unstruct_citation"]:
            f.write(l + "\n")


OUT_COLUMNS = [
    "DOI",
    "PMCID",
    "PMID",
    "URL",
    "year",
    "container-title",
    "title",
    "author_str",
]


def remove_trailing_punctuation(x):
    if pd.notna(x):
        return x[:-1] if x[-1] in [".", ";", ":"] else x
    else:
        return np.nan


def create_author_str(names):
    name_str = ""
    if names is np.nan:
        pass
    elif "literal" in names[0]:
        name_str = names[0]["literal"]
    else:
        if type(names) == list:
            for pos, n in enumerate(names):
                if "family" in n:
                    name_str = name_str + n["family"]
                if "given" in n:
                    name_str = name_str + ", " + n["given"]
                if pos < len(names) - 1:
                    name_str = name_str + "; "
    return name_str


def extract_year(date):
    year = None

    if pd.notna(date):
        year = date[0:4]
        if year.isdigit():
            return int(year)
        else:
            return None


def process_unstruct_refs(input_f, structured_refs_f, structured_f):
    """Processes JSON output from `anystyle`.

    1. Fixes DOI by removing unwanted trailing characters
    2. Constructs author strings from anystyle output
    3. Convert dates to years
    4. Return selection of columns
    """

    df = pd.read_json(
        open(structured_refs_f, "r"), dtype={"PMCID": object, "PMID": object},
    )
    # Fix DOIs (remove trailing periods)
    df["DOI"] = df["DOI"].map(remove_trailing_punctuation)

    # Process author name strings
    for ix, r in df.iterrows():
        name_str = create_author_str(r["author"])
        df.loc[ix, "author_str"] = name_str

    # Process date
    for ix, r in df.iterrows():
        year = extract_year(r["issued"])
        df.loc[ix, "year"] = year

    parsed = df[OUT_COLUMNS]

    logger.debug("Process structured references.")
    pubs = pd.read_csv(input_f, index_col="article_id")

    logger.debug("Merge with data from granting agency")
    pubs = pubs.join(parsed)

    logger.debug("Write output")
    pubs.to_csv(structured_f)
