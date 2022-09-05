from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import math
import json
import model
from database import DataBase
from user import post_user
from user import get_user

# DBの接続
db = DataBase()
search_locations = db.get_collection(collection_name="search_locations")
file_data = db.get_collection(collection_name="file_data")

app = FastAPI()

# CORSの設定
origins = [
    "http://localhost:3000",
    "https://lemon-bush-0663dd310.1.azurestaticapps.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# テストページを表示する関数
@app.get("/")
def hello():
    return {"hello" : "Hello World"}

# 投稿したページをタグから検索して表示する関数
@app.get("/page")
def get_page():

    search_result = {"kankou": [], "gurume": [], "tamasanpo":[], "omiyage":[]}

    tags  = ["kankou", "gurume", "tamasanpo" ,"omiyage"]
    page_names:dict = {"kankou": [], "gurume": [], "tamasanpo":[], "omiyage":[]}

    # 該当するタグのページの名前をDBから検索する
    for tag in tags:
        finds = file_data.find({"tag" : tag}, {"_id": False})
        for find in list(finds):
            page_names[tag].append(find["file_name"])

    # 検索されたページの名前から該当するページのデータをDBから取得する
    for tag in page_names:
        for page_name in page_names[tag]:
            page_data =  get_one_page(page_id=page_name)
            search_result[tag].append(page_data)

    return search_result

# 1つの投稿されたファイルのメタデータ情報を表示する関数
@app.get("/page/{page_id}")
def get_one_page(page_id :int=1):
    # 指定したページ番号から情報を取得する
    search_result: dict = file_data.find_one({"file_name" : page_id}, {"_id" : False})

    # 写真を取り出す
    with open("./pictures.json", mode="r") as f:
        j = json.load(f)
    search_result["image"] = j[str(page_id)]

    return search_result

# マップにピンを表示するための情報を与える関数
@app.get("/map")
async def get_location(myx:float, myy:float):

    # 配列の初期化
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
    display_num:int = 5 if (len(dists) > 5) else len(dists)
    
    # 距離が短い順に表示数の数だけ抜き出す
    sorted_dists = sorted(dists)
    for i in range(display_num):
        index = dists.index(sorted_dists[i])+1
        search_result.append(index)

    return {"result": search_result}

# 新しいメタデータを追加するための関数
@app.post("/page")
def post_page(page: model.Page):

    # DBからデータ数を読み取る
    finds_num:int = file_data.count_documents({})
    
    # 新しいページ番号の作成
    next_files_num: int = finds_num + 1
    
    page_x:float = page.other.location.x
    page_y:float = page.other.location.y

    # 受けとったjsonデータから新しいページを作成する
    new_page = {
        "file_name": next_files_num,
        "title": page.title,
        "tag": page.tag,
        "text": page.text,
        "other": {
            "user": page.other.user,
            "location": {
                "x": page_x,
                "y": page_y
            },
            "good": 0
        },
        "image" : page.image
    }

    # 新しく作成したデータをDBに追加
    result = file_data.insert_one(new_page)

    return result

# ユーザーを情報を返す
@app.get("/user/{user_id}")
def g_user(user_id: int = 1):
    return get_user(user_id)

# ユーザーの追加する
@app.post("/user")
def p_user(user: model.User):
    return post_user(user)