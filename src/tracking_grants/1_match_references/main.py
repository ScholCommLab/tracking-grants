# -*- coding: utf-8 -*-
from tracking_grants.utils.logging import logger

from .run_matcher import run as run_matcher
from .process_matches import run as process_matches


def run_all():
    logger.info("Matching references with articles")

    run_matcher()
    process_matches()