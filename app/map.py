from database import DataBase
import math

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
    