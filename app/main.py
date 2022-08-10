from fastapi import FastAPI
import json
import random

app = FastAPI()

@app.get("/")
def hello():
    return {"hello" : "Hello World"}

# 投稿したページをタグから検索して表示する関数
@app.get("/page")
async def get_page(tag: str="kankou"):
    data = "./data.json"
    search ="./search.json"

    search_result = []
    result = dict()

    # タグから該当するファイルを検索する
    with open(search, mode="r", encoding="utf-8") as f:
        jn = json.loads(f.read())["tags"]
        num = jn[tag]["num"]
        file = jn[tag]["file"]

        # 10個ファイルを検索する
        for i in range(10):
            rand = random.randint(0,num-1)
            search_result.append(file[rand])

    # 該当したファイルのメタデータを辞書に保存する
    with open(data, mode="r", encoding="utf-8") as f:
        d = json.loads(f.read())
        for i in search_result:
            result[str(i)] = d[str(i)]

    # 該当するファイルのメタデータを返す
    return result

# マップにピンを表示するための情報を与える関数
@app.get("/map")
def get_location(x:int, y:int):

    # return {"1.png":{"tag":"kankou","location":[100, 120]}}
    return {"x": x, "y": y}

