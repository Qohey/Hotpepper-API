# -*- coding: utf-8 -*-

import requests
from icecream import ic

class API():
    def __init__(self, url, api_key, table):
        self.url=url
        self._api_key = api_key
        self.table = table

    def get(self, format, **param):
        url = self.url.format(TABLE=self.table)
        payload = {"key":self._api_key, "format":format}
        payload.update(**param)
        res = requests.get(url=url, params=payload)
        return res.status_code, res

    def get_code(self, name, format):
        _, response = self.get(format)
        response = response.json()
        for col in response["results"][self.table]:
            if name in col["name"]:
                return col["code"]
        return ""
