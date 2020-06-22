# -*- coding: utf-8 -*-
import json

import pandas as pd
from habanero import Crossref
from ratelimit import limits, sleep_and_retry
from tqdm.auto import tqdm
from tracking_grants import articles_f, cr_metadata_f, email, tool_name
from tracking_grants.utils.logging import logger


@sleep_and_retry
@limits(calls=10, period=1)
def query_crossref(cr, dois):
    return cr.works(dois)


def main(articles_f, cr_metadata_f):
    # load articles
    articles = pd.read_csv(articles_f, index_col="article_id")
    cr = Crossref(mailto=email, ua_string=tool_name)

    dois = articles.DOI.tolist()
    # dois = dois[0:100]

    dois_per_call = 10
    r = list(range(0, len(dois), dois_per_call))
    r = r + [len(dois)]

    results = []
    for ix in tqdm(range(len(r) - 1), total=len(r) - 1):
        response = query_crossref(cr, dois[r[ix]:r[ix + 1]])
        results.extend(response)

    with open(cr_metadata_f, "w") as f:
        json.dump(results, f)


def run():
    print("hello")
    if not cr_metadata_f.exists():
        logger.info("\tCollecting Crossref metadata")
        main(articles_f, cr_metadata_f)
    else:
        logger.info("\tSkipped: Crossref metadata has been collected already.")
