from fastapi import FastAPI
import json
import random
import math

TEST_DATA_PATH = "./data.json"
TEST_SEARCH_DATA_PATH ="./search.json"

app = FastAPI()

@app.get("/")
def hello():
    return {"hello" : "Hello World"}

# 投稿したページをタグから検索して表示する関数
@app.get("/page")
async def get_page(tag: str="kankou"):

    search_result = []
    result = dict()

    # タグから該当するファイルを検索する
    with open(TEST_SEARCH_DATA_PATH, mode="r", encoding="utf-8") as f:
        jn = json.loads(f.read())["tags"]
        num = jn[tag]["num"]
        file = jn[tag]["file"]

        # 10個ファイルを検索する
        for i in range(10):
            rand = random.randint(0,num-1)
            search_result.append(file[rand])

    # 該当したファイルのメタデータを辞書に保存する
    with open(TEST_DATA_PATH, mode="r", encoding="utf-8") as f:
        d = json.loads(f.read())
        for i in search_result:
            result[str(i)] = d[str(i)]

    # 該当するファイルのメタデータを返す
    return result

# 1つの投稿されたファイルのメタデータ情報を表示する関数
@app.get("/page/{page_id}")
async def get_one_page(page_id=1):
    return {"page": page_id}

# マップにピンを表示するための情報を与える関数
@app.get("/map")
async def get_location(myx:float, myy:float):

    display_num: int = 0
    dists: float = []
    result: int = []

    # 保存されているメタデータから座標の距離を求める
    with open(TEST_SEARCH_DATA_PATH, mode="r", encoding="utf-8") as f:
        jn = json.loads(f.read())["locations"]

        for i in jn:
            dx: float = i[0] - myx
            dy: float = i[1] - myy
            dists.append(math.sqrt(dx*dx + dy*dy))

    # 表示数を決める
    display_num = 5 if (len(dists) > 5) else len(dists)
    
    # 距離が短い順に表示数の数だけ抜き出す
    s = sorted(dists)
    for i in range(display_num):
        result.append(dists.index(s[i]))

    return {"result": result}
