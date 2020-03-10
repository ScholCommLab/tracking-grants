# -*- coding: utf-8 -*-
from pathlib import Path

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm



def main():
    """Process and match results from Altmetric API
    """
    articles = pd.read_csv(data_dir / "interim/queried_ids", index_col="article_id")
    


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_dir = project_dir / "data"

    load_dotenv(find_dotenv())

    main()