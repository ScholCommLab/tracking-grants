# -*- coding: utf-8 -*-
import subprocess

from tracking_grants import crossref_f, one_ref_per_line
from tracking_grants import reference_matcher
from tracking_grants.utils.logging import logger


def match_refs_with_dois(input_f, output_f):
    """Run """
    cmd = [
        f"java",
        "-jar", str(reference_matcher),
        "-it", "file",
        "-i", input_f,
        "-o", output_f]
    subprocess.run(cmd)


def run():
    if not crossref_f.exists():
        logger.info("\tMatching references with DOIs on Crossref")
        match_refs_with_dois(one_ref_per_line, crossref_f)
    else:
        logger.info("\tSkipped: References have been already matched with DOIs.")
