# -*- coding: <utf-8 -*-
# -*- coding: utf-8 -*-
from tracking_grants.utils.logging import logger

from .query_pmids import run as query_pmids
from .crossref_metadata import run as crossref_metadata


def run_all():
    logger.info("Processing articles")

    crossref_metadata()
    query_pmids()
