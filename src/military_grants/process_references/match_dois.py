# -*- coding: utf-8 -*-
import subprocess

from military_grants import crossref_f, one_ref_per_line
from military_grants import reference_matcher
from military_grants.utils.logging import logger


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
        logger.info("\tSkipping. References have been already matched with DOIs.")
