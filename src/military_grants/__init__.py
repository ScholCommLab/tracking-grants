# -*- coding: <utf-8 -*-
from pathlib import Path

import seaborn as sns

# Plotting style
sns.set_style("darkgrid")
sns.set(rc={"figure.figsize": (8, 5)})

# Default locations
project_dir = Path(__file__).resolve().parents[2]
data_dir = project_dir / "data"

# External files
EXCEL = "external/input/"

# Temporary files
REFERENCES = "interim/references.csv"
ONE_REF_PER_LINE = "interim/one_ref_per_line.txt"
CROSSREF = "interim/reference_match_output.json"
ALTMETRIC = "interim/altmetric.csv"
WOS = "interim/wos.csv"

# Processed files
ARTICLES = "processed/articles.csv"
METRICS = "processed/metrics.csv"
