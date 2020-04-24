# Military Grants

> Exploration of publications funded through military grant programs

## Requirements

Make sure that the following programs are available on your machine.

- Python 3.6
- Poetry

## Instructions

Setup virtualenv within the project folder by running `poetry install`. This will setup a isolated development environment and install all required dependencies.

## Processing pipeline

### Preprocessing

**1. Export references from Excel sheets.**

Input: Folder with excel sheets (`data/external/input`)
Output: File with all references and grant IDs (`data/external/references.csv`)

### Process references

**2. Match references with DOIs**

Input: File with all references and grant IDs (`data/external/references.csv`)
Temporary: File with one reference per line (`data/interim/references.txt`)
Temporary: File containing all results from Crossref (`data/interim/reference_matching_results.json`)
Output: Articles with DOIs that are matched to references (`data/processed/articles.csv`)

### Process articles

**3. Enrich DOIs with Pubmed IDs**

Input: Articles (`data/processed/articles.csv`)
Output: Articles (`data/processed/articles.csv`)

### Collect metrics

**4a. Collect altmetrics**

Input: Articles (`data/processed/articles.csv`)
Temporary: Response from Altmetric (`data/interim/respose_altmetric.csv`)

**4b. Collect citations and disciplinary information**

Input: Articles (`data/processed/articles.csv`)
Temporary: Response from WoS (`data/interim/respose_wos.csv`)

**4c. Combine results**

Input: Results from Altmetric & WoS (`data/interim/respose_altmetric.csv`, `data/interim/respose_wos.csv`)
Output: Metrics (`data/processed/metrics.csv`)


### Create results

**5. Create results**

Input: Articles & metrics (`data/processed/metrics.csv`, `data/processed/articles.csv`)
Input: Report template (`notebooks/reports/*.ipynb`)
Output: Reports (`results/*.html`)

## Acknowledgement

Project based on the [cookiecutter data science project template](https://drivendata.github.io/cookiecutter-data-science/). #cookiecutterdatascience.