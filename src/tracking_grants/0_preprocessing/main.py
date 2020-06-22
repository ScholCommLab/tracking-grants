# -*- coding: utf-8 -*-
from .merge_excel_files import run
from tracking_grants.utils.logging import logger


def run_all():
    logger.info("Preprocessing")
    run()
