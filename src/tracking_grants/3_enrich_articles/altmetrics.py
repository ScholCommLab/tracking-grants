# -*- coding: utf-8 -*-
import pandas as pd
from pyaltmetric import Altmetric
from ratelimit import limits, sleep_and_retry
from tqdm.auto import tqdm
import json

from tracking_grants import altmetric_f, articles_f
from tracking_grants import altmetric_api_key, altmetric_call_limit
from tracking_grants.utils.logging import logger


@sleep_and_retry
@limits(calls=altmetric_call_limit, period=1)
def api_call(a, doi):
    try:
        return a.doi(doi)
    except Exception as e:
        return str(e)


def query_altmetric(articles_f, altmetric_f):
    articles = pd.read_csv(articles_f, index_col="article_id")
    a = Altmetric(altmetric_api_key)

    results = {}
    for doi in tqdm(articles.DOI):
        result = api_call(a, doi)
        results[doi] = result

    with open(altmetric_f, "w") as f:
        json.dump(results, f)


def run():
    if not altmetric_f.exists():
        logger.info("\tCollecting altmetric")
        query_altmetric(articles_f, altmetric_f)
    else:
        logger.info("\tSkipped: Altmetrics have been collected already.")
