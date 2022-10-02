from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
import math
import model
from database import DataBase
from user import User
from page import Page

# DBの接続
db = DataBase()
search_locations = db.get_collection(collection_name="search_locations")
file_data = db.get_collection(collection_name="file_data")

app = FastAPI()
page = Page()
user = User()

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
@app.get("/pages")
def get_pages(tag:str, pageNum:int):
    return page.get_pages(tag=tag, page_num=pageNum)

# 1つの投稿されたファイルのメタデータ情報を表示する関数
@app.get("/page/{page_id}")
def get_one_page(page_id :int=1):
    return page.get_one_page(page_id=page_id)

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
        # DBから取得した情報を変数に代入
        file_name = find["file_name"]
        title = find["title"]
        tag = find["tag"]
        image = find["image"]
        location = find["location"]

        # 自身の座標からの距離を求める
        x = location["x"]
        y = location["y"]
        dx = x - myx
        dy = y - myy
        r = math.sqrt(dx*dx + dy*dy)

        data.append({"file_name":file_name, "title":title, "tag": tag,  "x":x, "y":y, "r":r, "image": image})
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
def post_page(page_response: model.Page, token: str = Header(None)):
    user_id = User.get_id(token=token)
    return page.post_page(page=page_response, user_id=user_id)

# ユーザーの追加する
@app.post("/regist")
def regist(user_response: model.User):
    return user.regist(user=user_response)

# ログインして自身のIDを確認する
@app.post("/login")
def login(user_response: model.User):
    return user.login(user=user_response)

# ユーザーを情報を取得する
@app.get("/user")
def get_user(token: str = Header(None)):
    user_id = User.get_id(token=token)
    return user.get_user(user_id=user_id)

# お店のメダルを登録する
@app.put("/user")
def add_medal(shop: model.Shop, token: str = Header(None)):
    user_id = User.get_id(token=token)
    return user.add_medal(user_id, shop.shop_id)