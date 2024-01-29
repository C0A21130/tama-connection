import math
import random
from sqlalchemy.orm import Session

import model
from lib.page import Page

class Map():

    # 現在地から近くの情報を返却するメソッド
    def get_nearby_data(self, myx: float, myy: float, session: Session):
        # 出力結果を初期化
        result = {"page_count": 0, "locations": [], "pages": []}

        # DBから座標データが存在するもののみ取り出す
        pages = session.query(model.Pages).all()
        points = session.query(model.Points).all()

        # 位置情報が存在するページ数を結果に代入する
        for i, page in enumerate(pages):
            location = dict()
            result["pages"].append(Page.convert_page(page, points))
            dist = math.sqrt((page.lng - myx)**2 + (page.lat - myy)**2)
            result["pages"][i]["distance"] = dist
            location["x"] = page.lng
            location["y"] = page.lat
            location["distance"] = dist
            result["locations"].append({"location": location, "page_id": page.id})

        result["page_count"] = len(pages)

        # 近場のページソートで取り出す
        result["pages"] = sorted(result["pages"], key=lambda x:x["distance"])
        result["locations"] = sorted(result["locations"], key=lambda x:x["location"]["distance"])
        
        # 近場のページの結果を3つ代入する
        result["pages"] = result["pages"][0:3]
        result["locations"] = result["locations"][0:3]

        return result
    
    #　地区名から検索して返却するメソッド
    def get_district_form_data(self, session: Session):
        # 検索したい地区名を初期化
        district_list = {"稲城": [], "八王子": [], "東大和": [], "西東京": []}

        # 返却する結果の初期化
        result = {key : dict() for key in district_list}
        result["district_list"] = list(district_list.keys())

        # DBから投稿データを取り出す
        pages = session.query(model.Pages).all()
        points = session.query(model.Points).all()
        
        # 地区名が書かれている投稿データを検索をする
        for district in district_list:
            for page in pages:
                # DBオブジェクトから辞書に変換する
                p = Page.convert_page(page, points)               

                # 写真のタイトルと投稿場所とテキストに地区名が含まれているかを検索する
                try: 
                    if district in p["title"] or district in p["location_name"] or district in p["text"]:
                        district_list[district].append(p)
                except KeyError: # 投稿場所が記入されていないとき
                    if district in p["title"] or district in p["text"]:
                        district_list[district].append(p)
                    
        # 検索結果を返却する
        for district in district_list:
            try: # 検索結果が複数あるときはランダムに1つだけ返却値に設定する
                result[district] = random.choice(district_list[district])
            except IndexError: # 検索結果に存在しない場合は発見できなかったことを伝える
                result[district] = {"id": -1, "title": "見つかりませんでした", "tag": "kankou", "text": "", "user": -1, "location_name": "", "location": {"x":0, "y": 0}, "image": ""}
        return result