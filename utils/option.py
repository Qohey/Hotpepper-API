# -*- coding: utf-8 -*-
import sys
import argparse
from pprint import pprint

class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.opt = None

    def _initial(self):
        argv = sys.argv

        # ===============================================================
        #                     Common options
        # ===============================================================
        self.parser.add_argument("action", type=str, choices=["show", "exe"],   help="実行の種類")
        self.parser.add_argument("--api",  type=str, default="config/api.json", help="APIキーが保存されているファイルのパス")

        # ===============================================================
        #                     Show parameter options
        # ===============================================================
        if "show" in argv:
            self.parser.add_argument("type", type=str, choices=["area", "genre", "credit_card"], help="閲覧するオプションの種類")
            if "area" in argv:
                self.parser.add_argument("size", type=str, choices=["large", "middle", "small"], help="areaの大きさの種類")
                self.parser.add_argument("--pref", type=str, default="", help="middleを指定した時の都道府県")
                self.parser.add_argument("--city", type=str, default="", help="smallを指定した時の市町村")

            self.parser.add_argument("--keyword", type=str, default="", help="キーワード検索")

        # ===============================================================
        #                     Running options
        # ===============================================================
        if "exe" in argv:
            self.parser.add_argument("--name",  type=str, default="", help="飲食店名")
            self.parser.add_argument("--area",  type=str, default="", help="検索地域名")
            self.parser.add_argument("--genre", type=str, default="", nargs="+", help="ジャンル名")
            self.parser.add_argument("--free_drink", action="store_true", help="飲み放題有りで検索")
            self.parser.add_argument("--free_food", action="store_true", help="食べ放題有りで検索")
            self.parser.add_argument("--private_room", action="store_true", help="個室有りで検索")
            self.parser.add_argument("--card", action="store_true", help="クレジットカード可で検索")

    def _print(self):
        print("\n==================Options=================")
        pprint(vars(self.opt), indent=4)
        print("==========================================\n")

    def parse(self):
        self._initial()
        self.opt = self.parser.parse_args()
        self._print()
        return self.opt
