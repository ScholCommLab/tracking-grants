# -*- coding: <utf-8 -*-
from pathlib import Path
import os

from dotenv import load_dotenv, find_dotenv
import seaborn as sns

# =======================
# Load user configuration
# =======================
load_dotenv(find_dotenv())

# Plotting style
sns.set_style("darkgrid")
sns.set(
    rc={
        "font.family": "sans-serif",
        "font.size": 16.0,
        "text.usetex": False,
        "figure.figsize": (11.69, 8.27),
    }
)

# Load email address
tool_name = os.getenv("TOOL_NAME")
email = os.getenv("EMAIL")

# API keys
altmetric_api_key = os.getenv("ALTMETRIC_API_KEY")
ncbi_api_key = os.getenv("NCBI_API_KEY")

# Altmetric call limit
if not altmetric_api_key:
    altmetric_call_limit = 1
else:
    altmetric_call_limit = 10

# ===========
# Directories
# ===========
project_dir = Path(__file__).resolve().parents[2]
data_dir = project_dir / "data"

# Raw data (collected from CDMRP database)
# ----------------------------------------

input_folder = data_dir / "raw"  # contains all CSVs

# Interm files (Created by this package)
# --------------------------------------

# one reference per line in a .txt
one_ref_per_line = data_dir / "interim/one_ref_per_line.txt"

# output of the reference matcher
matched_articles_f = data_dir / "interim/reference_match_output.json"

# response from Altmetric.com
altmetric_f = data_dir / "interim/altmetric.json"

# additional metadata from Crossref
cr_metadata_f = data_dir / "interim/cr_metadata.json"

# unpaywall data
unpaywall_f = data_dir / "interim/unpaywall.csv"


# External files (gathered externally)
# ------------------------------------
wos_f = data_dir / "external/wos.csv"

# Processed files (final files used for analysis)
# -----------------------------------------------
references_f = data_dir / "processed/references.csv"
articles_f = data_dir / "processed/articles.csv"
metrics_f = data_dir / "processed/metrics.csv"
trials_f = data_dir / "processed/trials.csv"

# External software
# -----------------
reference_matcher = (
    project_dir / "crossref/search-based-ref-matching-1.1-jar-with-dependencies.jar"
)
