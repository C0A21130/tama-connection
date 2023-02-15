from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
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
    "https://tama-connect.com"
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
def get_location(myx:float, myy:float):
    # 結果を初期化
    result = {"page_count": 0, "locations": [], "pages": []}
    # DBから座標データが存在するもののみ取り出す
    finds = list(file_data.find({"location":{"$exists": True}}, {"_id" : False}))

    # 位置情報が存在するページ数を結果に代入する
    result["page_count"] = len(finds)
    # 距離だけを取り出して結果に代入する
    for find in finds:
        location = find["location"]
        location["distance"] = math.sqrt((location["x"] - myx)**2 + (location["y"] - myy)**2)
        result["locations"].append({"location": location, "page_id": find["page_id"]})
    # 近場のページを取り出す
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
@app.get("/users")
def add_medal(token: str = Header(None)):
    user_id = User.get_id(token=token)
    return user.get_users(user_id=user_id)

if __name__ == "__main__":
    uvicorn.run(app=app, port=5000)