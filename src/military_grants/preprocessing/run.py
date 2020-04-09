# -*- coding: utf-8 -*-
import subprocess
import sys
from pathlib import Path

from military_grants import (
    EXCEL,
    INPUT,
    ARTICLES,
    STRUCTURED_REFS,
    UNSTRUCTURED_REFS,
    data_dir,
)
from military_grants.utils.logging import logger

from .preprocessing import process_excel, process_input, process_unstruct_refs


def run():
    excel_f = data_dir / EXCEL
    input_f = data_dir / INPUT
    unstructured_refs_f = data_dir / UNSTRUCTURED_REFS
    structured_refs_f = data_dir / STRUCTURED_REFS
    articles_f = data_dir / ARTICLES

    if not Path(input_f).exists():
        logger.info("Process Excel file")
        process_excel(excel_f, input_f)
    else:
        logger.info("Skipping: Excel file has already been processed")

    if not Path(unstructured_refs_f).exists():
        logger.info("Creating temp file with one reference per line.")
        process_input(input_f, unstructured_refs_f)
    else:
        logger.info("Skipping: Temporary file with one reference per line exists.")

    if not Path(structured_refs_f).exists():
        logger.info("Parse unstructured references with 'anystyle")

        cmd = f"anystyle -f csl parse {unstructured_refs_f} > {structured_refs_f}"
        try:
            logger.info("Running task: {}".format(cmd))
            subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
        except subprocess.CalledProcessError as e:
            sys.stderr.write(
                "[ERROR]: output = {}, error code = {}\n".format(e.output, e.returncode)
            )
            sys.exit()
    else:
        logger.info("Skipping: Unstructured references already exist.")

    if not Path(articles_f).exists():
        logger.info("Processing the structured references")
        process_unstruct_refs(input_f, structured_refs_f, articles_f)
    else:
        logger.info("Skipping: Structured references have been already processed")
