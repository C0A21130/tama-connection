from fastapi import FastAPI
from pydantic import BaseModel
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

class Location(BaseModel):
    x: float
    y: float

class Other(BaseModel):
    user: str
    location_information: Location

# put_page関数の受け取るjsonデータの型
class Page(BaseModel):
    title: str
    tag: str
    text: str
    other: Other

# 新しいメタデータを追加するための関数
@app.post("/page")
async def put_page(page: Page):
    d: dict = dict()

    # テストデータから元のデータを読み取る
    with open(file=TEST_DATA_PATH, mode="r", encoding="utf-8") as f:
        d = json.loads(f.read())
    
    # 受けとったデータから新しいデータを作成して追加する
    next_files_num: int = d["files_num"]+1
    d["files_num"] = next_files_num
    page_x = page.other.location_information.x
    page_y = page.other.location_information.y
    new_d = {
        "title": page.title,
        "tag": page.tag,
        "text": page.title,
        "other": {
            "user": page.other.user,
            "location_information": {
                "x": page_x,
                "y": page_y
            }
        }
    }
    d[str(next_files_num)] = new_d

    # 新しく作成したデータをテストデータに書き込む
    with open(TEST_DATA_PATH, "w") as f:
        json.dump(d, f, indent=2)

    search_d: dict = dict()
    # テストの検索データから元のデータを読み取る
    with open(TEST_SEARCH_DATA_PATH, "r") as f:
        search_d = json.loads(f.read())
    
    # テストの検索データに受け取ったデータを追加する
    search_d["tags"][page.tag]["num"] += 1
    search_d["tags"][page.tag]["file"].append(int(next_files_num))
    search_d["locations"].append([page_x, page_y])

    # 受け取ったデータでテストの検索データを書き込む
    with open(TEST_SEARCH_DATA_PATH, "w") as f:
        json.dump(search_d, f, indent=2)

    return new_d