# -*- coding: utf-8 -*-
from military_grants.utils.logging import logger

from .altmetrics import run as collect_altmetrics
from .wos import run as collect_wos
from .process_metrics import run as process_metrics


def run_all():
    logger.info("Processing all articles")

    collect_altmetrics()
    collect_wos()
    process_metrics()