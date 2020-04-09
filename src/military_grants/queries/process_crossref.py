# -*- coding: utf-8 -*-
from pathlib import Path

import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv

from src.utils.mylogger import logger


@click.command()
@click.option("--score", default=80, help="Minimum score to match article with DOI")
def main(score):
    """ Match articles with results from Crossref with
    """
    # Load dataset
    articles = pd.read_csv(articles_file, index_col="article_id")
    crossref = pd.read_csv(crossref_file, index_col="article_id")

    article_metadata = articles[["type", "proposal_id"]]

    logger.info("Matching crossref information")
    article_metadata = article_metadata.join(
        crossref[crossref.score >= score][["DOI"]]
    )

    logger.info("Writing articles with matched IDs")
    article_metadata.to_csv(metadata_outfile)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    articles_file = data_dir / "interim/structured.csv"
    crossref_file = data_dir / "interim/_crossref.csv"

    metadata_outfile = data_dir / "processed/article_metadata.csv"

    load_dotenv(find_dotenv())

    main()
