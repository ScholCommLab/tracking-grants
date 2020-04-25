# -*- coding: <utf-8 -*-
from pathlib import Path
import os

from dotenv import load_dotenv, find_dotenv
import seaborn as sns

# Plotting style
sns.set_style("darkgrid")
sns.set(rc={"figure.figsize": (8, 5)})

config = load_dotenv(find_dotenv())

altmetric_api_key = os.getenv("ALTMETRIC_API_KEY")
# Altmetric call limit
if not altmetric_api_key:
    altmetric_call_limit = 1
else:
    altmetric_call_limit = 10

# Directories
project_dir = Path(__file__).resolve().parents[2]

# External software
reference_matcher = (
    project_dir / "crossref/search-based-ref-matching-1.1-jar-with-dependencies.jar"
)

# Data
data_dir = project_dir / "data"

# External data
input_folder = data_dir / "external"

# Temporary files
one_ref_per_line = data_dir / "interim/one_ref_per_line.txt"
crossref_f = data_dir / "interim/reference_match_output.json"
altmetric_f = data_dir / "interim/altmetric.json"
wos_f = data_dir / "interim/wos.json"

# Processed files
references_f = data_dir / "processed/references.csv"
articles_f = data_dir / "processed/articles.csv"
metrics_f = data_dir / "processed/metrics.csv"
