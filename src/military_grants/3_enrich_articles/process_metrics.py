# -*- coding: utf-8 -*-
import json

import pandas as pd
from military_grants import altmetric_f, metrics_f, wos_f
from military_grants.utils.logging import logger


def process_metrics(altmetric_f, wos_f, metrics_f):
    """Merge data from Altmetric and WoS."""
    altmetric = pd.DataFrame.from_dict(
        json.loads(altmetric_f.read_text()), orient="columns"
    ).T
    wos = pd.read_csv(wos_f, index_col="doi")

    altmetric.join(wos).to_csv(metrics_f)


def run():
    if not metrics_f.exists():
        logger.info("\tProcessing collected altmetrics and data from the WoS.")
        process_metrics(altmetric_f, wos_f, metrics_f)
    else:
        logger.info("\tSkipped: Metrics have already been processed and exported.")
