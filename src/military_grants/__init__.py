# -*- coding: <utf-8 -*-
import os
from pathlib import Path

import seaborn as sns
from dotenv import find_dotenv, load_dotenv

# Default locations
project_dir = Path(__file__).resolve().parents[2]
data_dir = project_dir / "data"

# Plotting style
sns.set_style("darkgrid")
sns.set(rc={"figure.figsize": (8, 5)})

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())
CR_THRESH = int(os.getenv("cr_thresh"))

# All constant files
EXCEL = os.getenv("EXCEL")
INPUT = os.getenv("INPUT")
UNSTRUCTURED_REFS = os.getenv("UNSTRUCTURED_REFS")
STRUCTURED_REFS = os.getenv("STRUCTURED_REFS")
ARTICLES = os.getenv("ARTICLES")
