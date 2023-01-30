from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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

# CORSの接続許可
origins = [
    "http://localhost:3000",
    "http://tk2-123-61896.vs.sakura.ne.jp"
]

# CORSの設定
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

# タグから投稿したページを検索して表示する関数
@app.get("/pages")
def get_pages(tag:str, pageNum:int):
    return page.get_pages(tag=tag, page_num=pageNum)

# 1つの投稿されたデータ情報を表示する関数
@app.get("/page/{page_id}")
def get_one_page(page_id :int=1):
    return page.get_one_page(page_id=page_id)

# 新しい投稿データを追加するための関数
@app.post("/page")
def post_page(page_response: model.Page, token: str = Header(None)):
    user_id = User.get_id(token=token)
    return page.post_page(page=page_response, user_id=user_id)

# 投稿データの更新
@app.put("/page/{page_id}")
def put_page(page_id: int, page_response:model.Page, token = Header(None)):
    user_id = User.get_id(token=token)
    return page.put_page(page_id=page_id, page=page_response, user_id=user_id)

# 1つの投稿データを削除
@app.delete("/page/{page_id}")
def delete_page(page_id: int):
    return page.delete_page(page_id=page_id)

# マップにピンを表示するための情報を与える関数
@app.get("/map")
def get_location(myx:float, myy:float):
    result = {"page_count": 0, "locations": []}

    # DBから座標データが存在するもののみ取り出す
    finds = list(file_data.find({"location":{"$exists": True}}, {"_id" : False}))

    # 結果を代入
    result["page_count"] = len(finds)
    for find in finds:
        result["locations"].append({"location": find["location"], "page_id": find["page_id"]})

    return result

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

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)