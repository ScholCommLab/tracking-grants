# Military Grants

> Exploration of publications funded through military grant programs

## Requirements

Make sure that the following programs are available on your machine.

- Python 3.6
- Poetry
- anystyle

## Instructions

1. Setup virtualenv within the project folder by running `poetry install`. This will setup a isolated development environment and install all required dependencies.

2. Fill in your altmetrics key in a file called `.env` in the following format
  
    ```bash
    altmetric_key = [your_key]
    ```

    or you can simply run the following command `echo "altmetric_key = [your_key]" >> .env`

3. Run make recipes to reproduce results
   1. Run `make get_data` to import data from Zenodo/Dataverse
   2. Run `make data` to re-run data processing pipelines
   3. Run `make reports` to create figures and html reports

## Acknowledgement

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>