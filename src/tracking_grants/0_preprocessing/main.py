# -*- coding: utf-8 -*-
from .process_input_files import run as process_input_files
from tracking_grants.utils.logging import logger


def run_all():
    logger.info("Preprocessing")
    process_input_files()
