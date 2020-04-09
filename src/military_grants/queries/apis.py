# -*- coding: utf-8 -*-
"""
This module contains various classes that help to access APIs.
"""

import requests


class CrossrefAPI:
    def __init__(self):
        self.cr_api = "https://api.crossref.org/works"
        self.params = {
            "query.bibliographic": None,
            "rows": 1,
            "mailto": "asura_enkhbayar@sfu.ca",
        }

    def query(self, citation):
        self.params["query.bibliographic"] = citation
        return requests.get(self.cr_api, params=self.params)


class NCBIAPI:
    def __init__(self):
        self.ncbi_api = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
        self.params = {
            "ids": None,
            "idtype": "doi",
            "format": "json",
            "email": "asura_enkhbayar@sfu.ca",
            "tool": "ScholCommLab Military Grants",
        }

    def query(self, doi):
        self.params["ids"] = [doi]
        return requests.get(self.ncbi_api, params=self.params)
