from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
import model
from database import DataBase
from user import User
from page import Page
from map import Map
from point import Point

# DBの接続
db = DataBase()
search_locations = db.get_collection(collection_name="search_locations")
file_data = db.get_collection(collection_name="file_data")

app = FastAPI()
page = Page()
user = User()
map = Map()
point = Point()

# CORSの接続許可
origins = [
    "http://localhost:3000"
]

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# gzipの設定
app.add_middleware(GZipMiddleware, minimum_size=1000)

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
def get_location(myx:float, myy:float, request="nearby"):
    # ユーザーのリクエストによって分岐
    if request == "district": # 地区名から検索した情報が欲しいとき
        return map.get_district_form_data()
    elif request == "nearby": # 近場の情報が欲しいとき
        return map.get_nearby_data(myx=myx, myy=myy)
    else:
        return "Error"

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

# ユーザーのパスワードを再設定する
@app.put("/user")
def put_user(user_response: model.User, token: str = Header(None)):
    user_id = User.get_id(token=token)
    return user.put_user(user_id=user_id, user=user_response)

# お店のメダルを登録する
@app.get("/users")
def get_users(token: str = Header(None)):
    user_id = User.get_id(token=token)
    return user.get_users(user_id=user_id)

# いいねや行ってみた、行ったことがあるを追加する
@app.put("/point")
def put_point(page_id:int, status: str, token: str = Header(None)):
    user_id = User.get_id(token=token)
    return point.increment_status(page_id=page_id, user_id=user_id, status=status)

@app.delete("/point")
def delete_point(page_id: int, status: str, token: str = Header(None)):
    user_id = User.get_id(token=token)
    return point.decrease_status(page_id=page_id, user_id=user_id, status=status)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)