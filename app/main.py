from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import random
import math

TEST_DATA_PATH = "./data.json"
TEST_SEARCH_DATA_PATH ="./search.json"

client = MongoClient(host="mongo", port=27017, username="root", password="password")
db = client["test_db"]

search_tags = db["search_tags"]
search_locations = db["search_locations"]
file_data = db["file_data"]

app = FastAPI()

@app.get("/")
def hello():
    return {"hello" : "Hello World"}

# 投稿したページをタグから検索して表示する関数
@app.get("/page")
def get_page(tag: str="kankou"):

    # 検索した結果を保存するリスト
    search_result: List[int] = []
    
    # 該当するタグのファイル名をDBから検索する
    find = search_tags.find_one({"tag" : tag}, {"_id": False})

    # 検索した結果からファイル数とファイルを取り出す
    files: List[int] = find["files"]
    num: int = len(files)

    # 10個ランダムで取り出す
    if num!=0:
        for i in range(num):
            rand: int = random.randint(0, num-1)
            search_result.append(files[rand])
    else:
        search_result = []

    # 該当するファイルのメタデータを返す
    return {"num" : num, "files" : search_result}

# 1つの投稿されたファイルのメタデータ情報を表示する関数
@app.get("/page/{page_id}")
def get_one_page(page_id :int=1):
    search_result: dict = file_data.find_one({"file_name" : page_id}, {"_id" : False})
    return search_result

# マップにピンを表示するための情報を与える関数
@app.get("/map")
async def get_location(myx:float, myy:float):

    display_num: int = 0
    dists: List[float] = []
    search_result: List[int] = []

    # 保存されているメタデータから座標の距離を求める
    find: dict = search_locations.find_one({}, {"_id" : False})

    # 自身の座標と写真の座標との距離を求める
    for f in find["locations"]:
        dx: float = f[0] - myx
        dy: float = f[1] - myy
        dists.append(math.sqrt(dx*dx + dy*dy))

    # 表示数を決める
    display_num = 5 if (len(dists) > 5) else len(dists)
    
    # 距離が短い順に表示数の数だけ抜き出す
    sorted_dists = sorted(dists)
    for i in range(display_num):
        index = dists.index(sorted_dists[i])+1
        search_result.append(index)

    return {"result": search_result}

class Location(BaseModel):
    x: float
    y: float

class Other(BaseModel):
    user: str
    location: Location

# put_page関数の受け取るjsonデータの型
class Page(BaseModel):
    title: str
    tag: str
    text: str
    other: Other

# 新しいメタデータを追加するための関数
@app.post("/page")
async def put_page(page: Page):

    # DBからデータ数を読み取る
    find: dict = file_data.find_one({"file_name": 0}, {"_id" : False})
    
    # 新しいページ番号の作成
    next_files_num: int = find["files_num"]+1
    
    page_x:float = page.other.location.x
    page_y:float = page.other.location.y

    # 受けとったjsonデータから新しいページを作成する
    new_page = {
        "file_name": next_files_num,
        "title": page.title,
        "tag": page.tag,
        "text": page.title,
        "other": {
            "user": page.other.user,
            "location_information": {
                "x": page_x,
                "y": page_y
            },
            "good": 0
        }
    }

    # 新しく作成したデータをデータに書き込む
    file_data.insert_one(new_page)
    file_data.update_one({"file_name": 0}, {"$set":{"files_num": next_files_num}})

    # タグ検索用DBに要素の追加
    search_tags.update_one({"tag":page.tag}, {"$push": {"files":next_files_num}})

    # 位置情報検索用DBに要素の追加
    search_locations.update_one({}, {"$push":{"locations":[page_x,page_y]}})

    return new_page