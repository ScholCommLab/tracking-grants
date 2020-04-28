# -*- coding: <utf-8 -*-
from pathlib import Path
import os

from dotenv import load_dotenv, find_dotenv
import seaborn as sns

# Load configuration
load_dotenv(find_dotenv())

# Plotting style
sns.set_style("darkgrid")
sns.set(rc={"figure.figsize": (8, 5)})

# Configure altmetric key
altmetric_api_key = os.getenv("ALTMETRIC_API_KEY")

# Altmetric call limit
if not altmetric_api_key:
    altmetric_call_limit = 1
else:
    altmetric_call_limit = 10

# Directories
project_dir = Path(__file__).resolve().parents[2]
data_dir = project_dir / "data"

# Raw data from CDMRP
input_folder = data_dir / os.getenv("INPUT_FOLDER")

# Temporary files
one_ref_per_line = data_dir / os.getenv("INPUT_FOLDER")
crossref_f = data_dir / os.getenv("CROSSREF")
altmetric_f = data_dir / os.getenv("ALTMETRIC")
wos_f = data_dir / os.getenv("WOS")

# Processed files
references_f = data_dir / os.getenv("REFERENCES")
articles_f = data_dir / os.getenv("ARTICLES")
metrics_f = data_dir / os.getenv("METRICS")

# External software
reference_matcher = (
    project_dir / "crossref/search-based-ref-matching-1.1-jar-with-dependencies.jar"
)