# Military Grants

> Exploration of publications funded through military grant programs

## Minimum requirements

- [Python 3.6](https://www.python.org/downloads/)
- [Java](https://java.com/en/download/) (required to run reference matching)

I strongly recommend to use [Poetry](https://python-poetry.org/docs/) to manage dependencies. Furthermore, Poetry provides entry points to comfortably run processing pipelines.

## Instructions

To get started simply execute

    git clone https://github.com/ScholCommLab/military-grants
    cd military-grants
    poetry install

This will create an isolated virtual environment in your project folder and install all required dependencies.

The processing pipeline is available as follows:

1. `poetry run preprocessing`
2. `poetry run references`
3. `poetry run articles`
4. `poetry run metrics`
5. `poetry run reports`

## Processing pipeline

### Preprocessing

**1. Export references from Excel sheets.**

- Input: Folder with excel sheets (`data/external/input`)
- Output: File with all references and grant IDs (`data/external/references.csv`)

### Process references

**2. Match references with DOIs**

- Input
  - File with all references and grant IDs (`data/external/references.csv`)
- Output
  - Articles with DOIs that are matched to references (`data/processed/articles.csv`)
  - *Interim:* File with one reference per line (`data/interim/references.txt`)
  - *Interim:* File containing all results from Crossref (`data/interim/reference_matching_results.json`)

### Process articles

**3. Enrich DOIs with Pubmed IDs**

- Input
  - Articles (`data/processed/articles.csv`)
- Output
  - Articles (`data/processed/articles.csv`)

### Collect metrics

**4a. Collect altmetrics**

- Input
  - Articles (`data/processed/articles.csv`)
- Output
  - *Interim:* Response from Altmetric (`data/interim/respose_altmetric.csv`)*

**4b. Collect citations and disciplinary information**

- Input
  - Articles (`data/processed/articles.csv`)
- Output
  - *Interim:* Response from WoS (`data/interim/respose_wos.csv`)

**4c. Combine results**

- Input
  - Results from Altmetric (`data/interim/respose_altmetric.csv`)
  - Results from WoS (`data/interim/respose_wos.csv`)
- Output
  - Metrics (`data/processed/metrics.csv`)

### Create results

**5. Create results**

- Input
  - Articles (`data/processed/articles.csv`)
  - Metrics (`data/processed/metrics.csv`)
  - Report template (`notebooks/reports/*.ipynb`)
- Output
  - Reports (`results/*.html`)

## Acknowledgement

We want to thank [Dominika Tkaczyk](https://gitlab.com/dtkaczyk) for all the help. We are also using [this project](https://gitlab.com/crossref/search_based_reference_matcher) to run the advanced reference matching methods described in [this blog post(https://www.crossref.org/blog/matchmaker-matchmaker-make-me-a-match/)].

This project is based on the [cookiecutter data science project template](https://drivendata.github.io/cookiecutter-data-science/). #cookiecutterdatascience.