# -*- coding: utf-8 -*-
from pathlib import Path

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm

from pyaltmetric import Altmetric


def main():
    """Query Altmetric API with DOIs to retrieve additional metadata & altmetrics
    """
    a = Altmetric()

    articles = pd.read_csv(input_file, index_col="article_id")

    results = {}
    for ix, row in tqdm(articles.iterrows(), total=len(articles), desc="Altmetric API"):
        r = a.doi(row["CR_DOI_candidate"])
        if r:
            results[ix] = r

    altmetric_results = pd.DataFrame.from_dict(results).T
    altmetric_results.index.name = "article_id"
    altmetric_results.to_csv(altmetric_outfile)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    input_file = data_dir / "interim/queried_ids.csv"
    altmetric_outfile = data_dir / "interim/_altmetric.csv"

    load_dotenv(find_dotenv())

    main()
