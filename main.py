# -*- coding: utf-8 -*-
import json
from pathlib import Path
from utils.option import Options
from utils.api import API


if __name__ == "__main__":
    opt = Options().parse()
    api_key_file = Path(opt.api)
    with api_key_file.open() as f:
        json_content = json.load(f)
        API_KEY = json_content["HOTPEPPER_API_KEY"]
    URL = "http://webservice.recruit.co.jp/hotpepper/{TABLE}/v1/"

    if opt.action == "show":
        if opt.type == "area":
            print(f"\n================{opt.size} areas===============")
            if opt.size == "large":
                large_area = API(URL, API_KEY, "large_area")
                status, response = large_area.get("json")
                for col in response.json()["results"]["large_area"]:
                    print(col["name"])

            if opt.size == "middle":
                middle_area = API(URL, API_KEY, "middle_area")
                param = {"keyword":opt.keyword}
                if opt.pref != "":
                    large_area = API(URL, API_KEY, "large_area")
                    large_area_code = large_area.get_code(opt.pref, "json")
                    param.update({"large_area":large_area_code})
                status, response = middle_area.get("json", **param)
                for col in response.json()["results"]["middle_area"]:
                    print(col["name"])

            if opt.size == "small":
                small_area = API(URL, API_KEY, "small_area")
                param = {"keyword":opt.keyword}
                if opt.city != "":
                    middle_area = API(URL, API_KEY, "middle_area")
                    middle_area_code = middle_area.get_code(opt.city, "json")
                    param.update({"middle_area":middle_area_code})
                status, response = small_area.get("json", **param)
                for col in response.json()["results"]["small_area"]:
                    print(col["name"])
        else:
            print(f"\n================{opt.type}s===============")
            genre = API(URL, API_KEY, opt.type)
            param = {"keyword": opt.keyword}
            status, response = genre.get("json", **param)
            for col in response.json()["results"][opt.type]:
                print(col["name"])
        print("==========================================\n")

    if opt.action == "exe":
        gourmet = API(URL, API_KEY, "gourmet")
        param = {"name":opt.name, "free_drink":int(opt.free_drink), "free_food":int(opt.free_food), "private_room":int(opt.private_room), "card":int(opt.card)}
        if opt.area != "":
            area_code = API(URL, API_KEY, "large_area").get_code(opt.area, "json")
            area_size = "large_area"
            if area_code == "":
                area_code = API(URL, API_KEY, "middle_area").get_code(opt.area, "json")
                area_size = "middle_area"
            if area_code == "":
                area_code = API(URL, API_KEY, "small_area").get_code(opt.area, "json")
                area_size = "small_area"
        param.update({area_size:area_code})

        genre_codes = []
        for genre_name in opt.genre:
            code = API(URL, API_KEY, "genre").get_code(genre_name, "json")
            if code != "":
                genre_codes.append(code)
        param.update({"genre":",".join(genre_codes)})

        status, response = gourmet.get("json", **param)
        sum_count = int(response.json()["results"]["results_returned"])
        results_available = int(response.json()["results"]["results_available"])
        sum_count = int(response.json()["results"]["results_returned"])
        while sum_count <= results_available:
            print(f"{sum_count}/{results_available}")
            for col in response.json()["results"]["shop"]:
                print(f"{col['name']} : {col['urls']['pc']}")
            param.update({"start":sum_count+1})
            if sum_count == results_available:
                break
            key = input("次の10件を表示しますか？Y,N :")
            if key == "n" or key == "N":
                break
            status, response = gourmet.get("json", **param)
            sum_count += int(response.json()["results"]["results_returned"])
