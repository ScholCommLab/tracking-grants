# -*- coding: utf-8 -*-
import subprocess

from military_grants import CROSSREF, ONE_REF_PER_LINE, data_dir, project_dir
from military_grants import REFERENCE_MATCHER
from military_grants.utils.logging import logger


def match_refs_with_dois(input_f, output_f):
    """Run """
    cmd = [
        f"java",
        "-jar", str(REFERENCE_MATCHER),
        "-it", "file",
        "-i", input_f,
        "-o", output_f]
    response = subprocess.run(cmd)


def run():
    # Run Crossref reference_matcher
    input_f = data_dir / ONE_REF_PER_LINE
    output_f = data_dir / CROSSREF

    if not output_f.exists():
        logger.info("\tMatching references with DOIs on Crossref")
        match_refs_with_dois(input_f, output_f)
    else:
        logger.info("\tSkipping. References have been already matched with DOIs.")
