from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.orm import Session
import uvicorn
import model
import database
from lib.user import User
from lib.page import Page
from lib.map import Map
from lib.point import Point

app = FastAPI()
page = Page()
user = User()
map = Map()
point = Point()

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

def get_db():
    session = database.Session()
    try:
        yield session
    finally:
        session.close()

# テストページを表示する関数
@app.get("/")
def hello():
    return {"hello" : "Hello World"}

# タグから投稿したページを検索して表示する関数
@app.get("/pages")
def get_pages(tag:str, pageNum:int, session: Session = Depends(get_db)):
    return page.get_pages(tag=tag, page_num=pageNum, session=session)

# 1つの投稿されたデータ情報を表示する関数
@app.get("/page/{page_id}")
def get_one_page(page_id: int = 1, token: str = Header(None), session: Session = Depends(get_db)):
    result = dict()
    try:
        user_id = User.get_id(token=token)
        result = page.get_one_page(page_id=page_id, user_id=user_id, session=session)
    except:
        result = page.get_one_page(page_id=page_id, user_id=0, session=session)
    finally:
        if result == {}:
            raise HTTPException(status_code=404, detail=f"Article with id {page_id} not found")
        return result

# 新しい投稿データを追加するための関数
@app.post("/page")
def post_page(page_response: model.ResponsePage, token: str = Header(None), session: Session = Depends(get_db)):
    user_id = User.get_id(token=token)
    result = page.post_page(page=page_response, user_id=user_id, session=session)
    if not result:
        raise HTTPException(status_code=404, detail="upload error")

# 1つの投稿データを削除
@app.delete("/page/{page_id}")
def delete_page(page_id: int, session: Session = Depends(get_db)):
    result = page.delete_page(page_id=page_id, session=session)
    if not result:
        raise HTTPException(status_code=404, detail=f"No update article {page_id}")

# マップにピンを表示するための情報を与える関数
@app.get("/map")
def get_location(myx:float, myy:float, request="nearby", session: Session = Depends(get_db)):
    # ユーザーのリクエストによって分岐
    if request == "district": # 地区名から検索した情報が欲しいとき
        return map.get_district_form_data(session=session)
    elif request == "nearby": # 近場の情報が欲しいとき
        return map.get_nearby_data(myx=myx, myy=myy, session=session)
    else:
        raise HTTPException(status_code=404, detail="Not request prametar")

# ユーザーの追加する
@app.post("/regist")
def regist(user_response: model.ResponseUser, session: Session = Depends(get_db)):
    result = user.regist(user=user_response, session=session)
    if result != None:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"This Name existed {user_response.name}")

# ログインして自身のIDを確認する
@app.post("/login")
def login(user_response: model.ResponseUser, session: Session = Depends(get_db)):
    return user.login(user=user_response, session=session)

# 管理者ならばユーザー情報一覧を取得する
@app.get("/users")
def get_users(token: str = Header(None), session: Session = Depends(get_db)):
    user_id = User.get_id(token=token)
    result = user.get_users(user_id=user_id, sesstion=session)
    if result == None:
        raise HTTPException(status_code=404, detail="This account is not admin")
    else:
        return result

# ユーザーの名前と投稿データ一覧を取得する
@app.get("/user")
def get_user(token: str = Header(None), session: Session = Depends(get_db)):
    user_id = User.get_id(token=token)
    result = user.get_user(user_id=user_id, session=session)
    if result == None:
        raise HTTPException(status_code=404, detail="No user or pages")
    else:
        return result

# 管理者ならばユーザーのパスワードを再設定する
@app.put("/user")
def put_user(user_response: model.ResponseUser, token: str = Header(None), session: Session = Depends(get_db)):
    user_id = User.get_id(token=token)
    result = user.put_user(user_id=user_id, user=user_response, session=session)
    if result:
        return "Changed user password"
    else:
        raise HTTPException(status_code=404, detail=f"This account is not admin")

# ユーザーの情報を削除する
@app.delete("/user")
def del_user(name: str, token: str = Header(None), session: Session = Depends(get_db)):
    try:
        user_id = User.get_id(token=token)
    except:
        raise HTTPException(status_code=404, detail=f"This JWT in not enabled")
    result = user.del_user(name, user_id=user_id, session=session)
    if result != None:
        return f"Success to delete user id : {user_id}"

# いいねや行ってみた、行ったことがあるを追加する
@app.post("/point")
def put_point(page_id:int, status: str, token: str = Header(None), session: Session = Depends(get_db)):
    user_id = User.get_id(token=token)
    result = point.increment_status(page_id=page_id, user_id=user_id, status=status, session=session)
    if result:
        return f"papge-id {page_id} add {status}"
    else:
        raise HTTPException(status_code=404, detail=f"page-id {page_id} is added {status}")

# いいねや行ってみた、行ったことがあるを削除する
@app.put("/point")
def delete_point(page_id: int, status: str, token: str = Header(None), session: Session = Depends(get_db)):
    user_id = User.get_id(token=token)
    result = point.decrease_status(page_id=page_id, user_id=user_id, status=status, session=session)
    if result:
        return f"page-id {page_id} delete {status}"
    else:
        raise HTTPException(status_code=404, detail=f"Failed delete page-id {page_id} to {status}")

if __name__ == "__main__":
    uvicorn.run(app=app, port=5000)