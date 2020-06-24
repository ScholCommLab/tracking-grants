# -*- coding: utf-8 -*-
import json
import subprocess

import pandas as pd
from tqdm.auto import tqdm
from tracking_grants import (data_dir, matched_articles_f, one_ref_per_line,
                             reference_matcher, references_f)
from tracking_grants.utils.logging import logger


def process_input(input_f, references_f):
    """Read input file and export references as 1ref1line."""
    pubs = pd.read_csv(input_f)

    # Write references into text files for `anystyle`
    logger.debug("Writing unstructured references to txt")
    with open(references_f, "w") as f:
        for l in pubs["reference"]:
            f.write(l + "\n")


def run_matcher(input_f, output_f):
    """Run reference matcher algorithm implemented in java"""
    n_threads = 20

    cmd = [
        "java",
        "-jar",
        str(reference_matcher),
        "-it",
        "file",
        "-i",
        str(input_f),
        "-o",
        str(output_f),
        "-t",
        str(n_threads),
    ]
    subprocess.run(cmd)


def create_tempfiles(input_f):
    # Count lines in refs
    n_refs = 0
    with open(one_ref_per_line) as rf:
        n_refs = sum(1 for line in rf)

    # Prepare tempfiles
    batch_size = 500
    batches = list(range(0, n_refs, batch_size))
    tempfiles = [data_dir / f"interim/{i}.txt" for i in range(0, len(batches))]
    outfiles = [data_dir / f"interim/{i}.json" for i in range(0,len(batches))]

    # Remove old temp files
    for f in tempfiles:
        f.open("w")

    with open(one_ref_per_line) as rf:
        counter = 0
        file_count = 0
        for line in rf:
            if counter == batch_size:
                file_count = file_count + 1
                counter = 0

            with tempfiles[file_count].open("a") as file:
                if counter == 499:
                    file.write(line.strip())
                else:
                    file.write(line)

            counter = counter + 1

    return tempfiles, outfiles


def match_all_refs(one_ref_per_line, matched_articles_f):
    infiles, outfiles = create_tempfiles(one_ref_per_line)

    for fin, fout in tqdm(zip(infiles, outfiles)):
        run_matcher(fin, fout)

    # merge all outfiles
    output = []
    for fout in outfiles[0:4]:
        d = json.loads(fout.read_text())
        output = output + d

    # write output file
    with matched_articles_f.open("w") as f:
        json.dump(output, f)

    # delete temporary input and output files
    for fin, fout in zip(infiles, outfiles):
        fin.unlink()
        fout.unlink()


def run():
    if not one_ref_per_line.exists():
        logger.info("\tCreating temp file with one reference per line.")
        process_input(references_f, one_ref_per_line)
    else:
        logger.info("\tSkipped: Temporary file with one reference per line exists.")

    if not matched_articles_f.exists():
        logger.info("\tMatching references with DOIs on Crossref")
        match_all_refs(one_ref_per_line, matched_articles_f)
    else:
        logger.info("\tSkipped: References have been already matched with DOIs.")
