# -*- coding: utf-8 -*-
from military_grants.utils.logging import logger

from .export_references import run as export_refs
from .match_dois import run as match_dois
from .write_articles import run as write_articles


def run_all():
    logger.info("Processing all articles")

    export_refs()
    match_dois()
    write_articles()