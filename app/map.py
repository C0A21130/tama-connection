from database import DataBase
import math
import random

class Map():

    def __init__(self):
        self.db = DataBase()
        self.file_data = self.db.get_collection(collection_name="file_data")

    # 現在地から近くの情報を返却するメソッド
    def get_nearby_data(self, myx: float, myy: float):
        # 結果を初期化
        result = {"page_count": 0, "locations": [], "pages": []}
        # DBから座標データが存在するもののみ取り出す
        finds = list(self.file_data.find({"location":{"$exists": True}}, {"_id" : False}))

        # 位置情報が存在するページ数を結果に代入する
        result["page_count"] = len(finds)
        # 距離だけを取り出して結果に代入する
        for find in finds:
            location = find["location"]
            location["distance"] = math.sqrt((location["x"] - myx)**2 + (location["y"] - myy)**2)
            result["locations"].append({"location": location, "page_id": find["page_id"]})
        # 近場のページバブルソートで取り出す
        for i in range(len(result["locations"])):
            for j in range(len(result["locations"]) - i - 1):
                if result["locations"][j]["location"]["distance"] > result["locations"][j + 1]["location"]["distance"]:
                    tmp = result["locations"][j]
                    result["locations"][j] = result["locations"][j+1]
                    result["locations"][j+1] = tmp
        # 近場のページの結果を3つ代入する
        for find in finds:
            # 最も近場のページを追加
            if find["page_id"] == result["locations"][2]["page_id"]:
                result["pages"].append(find)
            # 次に近場のページを追加
            elif find["page_id"] == result["locations"][1]["page_id"]:
                result["pages"].append(find)
            # 3番目に近場のページを追加
            elif find["page_id"] == result["locations"][0]["page_id"]:
                result["pages"].append(find)

        return result
    
    #　地区名から検索して返却するメソッド
    def get_district_form_data(self):
        # 検索したい地区名を初期化
        district_list = {"稲城": [], "八王子": [], "東大和": [], "西東京": []}
        # 返却する結果の初期化
        result = {key : dict() for key in district_list}
        result["district_list"] = list(district_list.keys())
        # DBから投稿データを取り出す
        finds = self.file_data.find({}, {"_id": False})
        finds = list(finds)
        # 地区名が書かれている投稿データを検索をする
        for district in district_list:
            for find in finds:
                # 写真のタイトルと投稿場所とテキストに地区名が含まれているかを検索する
                try: 
                    if district in find["title"] or district in find["location_name"] or district in find["text"]:
                        district_list[district].append(find)
                except KeyError: # 投稿場所が記入されていないとき
                    if district in find["title"] or district in find["text"]:
                        district_list[district].append(find)
        # 検索結果を返却する
        for district in district_list:
            try: # 検索結果が複数あるときはランダムに1つだけ返却値に設定する
                result[district] = random.choice(district_list[district])
            except IndexError: # 検索結果に存在しない場合は発見できなかったことを伝える
                result[district] = {"id": -1, "title": "見つかりませんでした", "tag": "kankou", "text": "", "user": -1, "location_name": "", "location": {"x":0, "y": 0}, "image": ""}
        return result