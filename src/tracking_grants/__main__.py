# -*- coding: utf-8 -*-
from tracking_grants.utils.logging import logger

from .collect_metrics.main import run_all as metrics
from .preprocessing.main import run_all as preprocessing
from .process_articles.main import run_all as articles
from .process_references.main import run_all as references


def run():
    logger.info("+++ Running all processing steps at once.")

    preprocessing()
    references()
    articles()
    metrics()
