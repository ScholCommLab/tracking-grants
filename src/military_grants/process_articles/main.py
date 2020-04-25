# -*- coding: <utf-8 -*-
# -*- coding: utf-8 -*-
from military_grants.utils.logging import logger

from .query_pmids import run as query_pmids


def run_all():
    logger.info("=== Processing articles")

    query_pmids()
