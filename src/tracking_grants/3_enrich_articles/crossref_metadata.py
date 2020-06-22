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

    # Initialize client with UserAgent
    cr = Crossref(mailto=email, ua_string=tool_name)

    dois = articles.DOI.tolist()

    dois_per_call = 10
    r = list(range(0, len(dois), dois_per_call))
    r = r + [len(dois)]

    results = []
    for ix in tqdm(range(len(r) - 1), total=len(r) - 1, desc="Querying Crossref"):
        response = query_crossref(cr, dois[r[ix] : r[ix + 1]])
        results.extend(response)

    with open(cr_metadata_f, "w") as f:
        json.dump(results, f)


def process_crossref(cr_metadata_f, articles_f):
    results = json.loads(open(cr_metadata_f, "r").read())
    articles = pd.read_csv(articles_f, index_col="article_id")

    direct_fields = [
        "ISSN",
        "container-title",
        "publisher",
        "is-referenced-by-count",
        "references-count",
        "subject",
    ]
    transform_fields = [
        "authors_count",
    ]
    date_fields = ["created", "deposited", "indexed", "published-online", "issued"]

    df = pd.DataFrame(
        index=articles.DOI.tolist(),
        columns=direct_fields + transform_fields + date_fields,
    )

    for r in tqdm(results, total=len(results), desc="Processing results"):
        resp = r["message"]
        doi = resp["DOI"]

        for direct_f in direct_fields:
            if direct_f in resp:
                df.loc[doi, direct_f] = resp[direct_f]

        # authors
        if "author" in resp:
            df.loc[doi, "authors_count"] = len(resp["author"])

        for date_f in date_fields:
            if date_f in resp:
                df.loc[doi, date_f] = resp[date_f]["date-parts"][0][0]

    df = df.replace(0, np.nan)
    df = df.rename(
        columns={
            "container-title": "journal_name",
            "is-referenced-by-count": "coci_citations",
            "references-count": "references",
            "subject": "cr_subject",
        }
    )

    articles.merge(df, left_on="DOI", right_index=True).to_csv(articles_f)


def run():
    print("hello")
    if not cr_metadata_f.exists():
        logger.info("\tCollecting Crossref metadata")
        main(articles_f, cr_metadata_f)
        process_crossref(articles_f, cr_metadata_f)
    else:
        logger.info("\tSkipped: Crossref metadata has been collected already.")
