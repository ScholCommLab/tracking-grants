# -*- coding: <utf-8 -*-
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
import seaborn as sns

# Plotting style
sns.set_style("darkgrid")
sns.set(rc={"figure.figsize": (8, 5)})

config = load_dotenv(find_dotenv())

# Default locations
project_dir = Path(__file__).resolve().parents[2]
data_dir = project_dir / "data"

REFERENCE_MATCHER = (
    project_dir / "crossref/search-based-ref-matching-1.1-jar-with-dependencies.jar"
)

# External files
EXCEL = "external/"

# Temporary files
ONE_REF_PER_LINE = "interim/one_ref_per_line.txt"
CROSSREF = "interim/reference_match_output.json"
ALTMETRIC = "interim/altmetric.csv"
WOS = "interim/wos.csv"

# Processed files
REFERENCES = "processed/references.csv"
ARTICLES = "processed/articles.csv"
METRICS = "processed/metrics.csv"
