# -*- coding: utf-8 -*-
import json
import pandas as pd
from tracking_grants.utils.logging import logger
from tracking_grants import references_f, matched_articles_f, articles_f


def export_articles(references_f, matches_f, articles_f):
    # Load files
    refs = pd.read_csv(references_f)
    matches = pd.DataFrame.from_dict(json.loads(matched_articles_f.read_text()))

    # Merge references and matched responses from crossref by reference ID
    articles = refs.merge(
        matches[["score", "DOI"]], left_on="reference_id", right_index=True
    )

    # Drop all references without a match
    articles = articles[articles.DOI.notna()]

    # Remove duplicates
    output_cols = ["reference_id", "grant_id", "program", "score", "DOI"]
    articles = articles[output_cols].drop_duplicates()

    # Write file
    articles.to_csv(articles_f, index=False)


def run():
    if not articles_f.exists():
        logger.info("\tWriting matched articles and reference metadata.")
        export_articles(references_f, matched_articles_f, articles_f)
    else:
        logger.info("\tSkipped: Articles and references have already been exported.")
