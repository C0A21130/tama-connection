from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import math
import model
from database import DataBase
from user import User

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

    return search_result

# マップにピンを表示するための情報を与える関数
@app.get("/map")
def get_location(myx:float, myy:float):
    dists = []
    data = []
    search_result = []

    # 保存されているメタデータから座標の距離を求める
    finds = file_data.find({"location":{"$exists": True}}, {"_id" : False})

    # 自身の座標と写真の座標との距離を求める
    for find in list(finds):
        file_name = find["file_name"]
        location = find["location"]
        x = location["x"]
        y = location["y"]
        dx = x - myx
        dy = y - myy
        r = math.sqrt(dx*dx + dy*dy)
        data.append({"file_name":file_name, "x":x, "y":y, "r":r})
        dists.append(r)
    
    # 距離が短い順に並べる
    dists_sort = sorted(dists)
    for dist in dists_sort:
        for d in data:
            if dist==d["r"]:
                search_result.append(d)

    return search_result

# 新しいメタデータを追加するための関数
@app.post("/page")
def post_page(page: model.Page):

    # DBからデータ数を読み取る
    finds_num:int = file_data.count_documents({})
    
    # 新しいページ番号の作成
    next_files_num: int = finds_num + 1
    
    page_x:float = page.location.x
    page_y:float = page.location.y

    # 受けとったjsonデータから新しいページを作成する
    new_page = {
        "file_name": next_files_num,
        "title": page.title,
        "tag": page.tag,
        "text": page.text,
        "user": page.user,
        "location": {
            "x": page_x,
            "y": page_y
        },
        "image" : page.image
    }

    # 新しく作成したデータをDBに追加
    result = file_data.insert_one(new_page)

    return result

# ユーザーの追加する
@app.post("/regist")
def regist(user: model.User):
    user_data = User()
    return user_data.regist(user=user)

# ログインして自身のIDを確認する
@app.post("/login")
def login(user: model.User):
    user_data = User()
    return user_data.login(user=user)

# ユーザーを情報を取得する
@app.get("/user")
def get_user(token:str):
    user_data = User()
    return user_data.get_user(token=token)
