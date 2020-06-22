# -*- coding: utf-8 -*-
import pandas as pd

from military_grants import one_ref_per_line, references_f
from military_grants.utils.logging import logger


def process_input(input_f, references_f):
    """Read input file and export references as 1ref1line."""
    pubs = pd.read_csv(input_f)

    # Write references into text files for `anystyle`
    logger.debug("Writing unstructured references to txt")
    with open(references_f, "w") as f:
        for l in pubs["reference"]:
            f.write(l + "\n")


def run():
    if not one_ref_per_line.exists():
        logger.info("\tCreating temp file with one reference per line.")
        process_input(references_f, one_ref_per_line)
    else:
        logger.info("\tSkipped: Temporary file with one reference per line exists.")
