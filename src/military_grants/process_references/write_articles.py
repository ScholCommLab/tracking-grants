# -*- coding: utf-8 -*-
import json
import pandas as pd
from military_grants.utils.logging import logger
from military_grants import REFERENCES, CROSSREF, ARTICLES, data_dir


def export_articles(references_f, matches_f, articles_f):
    refs = pd.read_csv(references_f)
    matches = pd.DataFrame.from_dict(json.loads(matches_f.read_text()))

    # Load files
    refs = pd.read_csv(references_f, index_col="reference_id")
    matches = pd.DataFrame.from_dict(json.loads(matches_f.read_text()))
    matches.index.name = "reference_id"

    # Merge references and matched responses from crossref by reference ID
    merged = matches.merge(refs)

    # Drop all references without a match
    merged = merged[merged.DOI.notna()]
    merged.shape

    # Choose one reference per DOI (randomly the first one)
    # to get rid of typos in the reference
    articles = merged.reindex(merged.DOI.drop_duplicates().index)[
        ["DOI", "reference", "score", "type"]
    ]
    articles.shape

    # Deduplicate. Articles might have multiple references because of multiple grants
    n_grants = merged.groupby("DOI")["grant_id"].nunique()
    n_grants.name = "n_grants"
    articles = articles.merge(n_grants, left_on="DOI", right_index=True)

    # Reindex
    articles.index = range(0, len(articles))
    articles.index.name = "article_id"

    # Write file
    articles.to_csv(articles_f)


def run():
    references_f = data_dir / REFERENCES
    articles_f = data_dir / ARTICLES
    matches_f = data_dir / CROSSREF

    if not articles_f.exists():
        logger.info("\tWriting matched articles and reference metadata.")
        export_articles(references_f, matches_f, articles_f)
    else:
        logger.info("\tArticles and references have already been exported.")
