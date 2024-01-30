import os
from dotenv import load_dotenv
import datetime
import jwt
import hashlib
from sqlalchemy.orm import Session

import model
from lib.page import Page

load_dotenv("./.env")
KEY = os.getenv("KEY")

# ユーザー情報のクラス
class User:

    # JWTのトークンを生成する
    @classmethod
    def cleate_token(cls, user_id):
        dt_now = datetime.datetime.now()

        payload = {
            "id" : user_id,
            "ex" : dt_now.strftime("%Y-%m-%d %H:%M")
        }
        result = jwt.encode(payload, KEY, algorithm="HS256")
        return result

    # JWTトークンからユーザーIDを習得する
    @classmethod
    def get_id(cls, token):
        # JWTをデコードする
        data = jwt.decode(token, KEY, algorithms=["HS256"])
        
        # ユーザーIDの取得
        user_id = data["id"]
        return user_id

    # ユーザーの情報を追加
    def regist(self, user: model.ResponseUser, session: Session):
        # 入力内容をオブジェクトへ初期化
        new_user = model.Users(
            name = user.name,
            password = hashlib.sha256(f"{user.name}{user.password}".encode("UTF-8")).hexdigest(),
            admin = False,
            taxi = False
        )

        # DBへ入力されたユーザー名を検索
        find = session.query(model.Users).filter(model.Users.name == user.name).first()

        # 同じ名前の人が存在するか確認しいなければDBに追加する
        if (find == None):
            try:
                # DBにユーザーの情報を追加
                session.add(new_user)
                session.flush()
                session.commit()

                # JWTを作成
                token = User.cleate_token(new_user.id)
                return {"token" : token}
            except:
                session.rollback()

    # ユーザーがDBにあるか確認して存在すればJWTを返却する
    def login(self, user: model.ResponseUser, session: Session):
        # パスワードのハッシュ値を生成
        temp = f"{user.name}{user.password}"
        pasword = hashlib.sha256(temp.encode("UTF-8")).hexdigest()

        # DBからユーザー名とパスワードで検索
        find = session.query(model.Users).filter(model.Users.name == user.name, model.Users.password == pasword).first()
        
        # JWTトークンを再作成
        token = User.cleate_token(user_id=find.id)
        return {"token" : token}

    # ユーザーの情報をDBから削除する
    def del_user(self, name: str, user_id: int, session: Session):
        try:
            # DBからIDとユーザー名が一致していればユーザーを消去する
            session.query(model.Users).filter(model.Users.id == user_id, model.Users.name == name).delete()
            session.commit()
            return user_id
        except:
            session.rollback()

    # 管理者な全ユーザーの情報を返す関数
    def get_users(self, user_id: int, sesstion: Session) -> dict:
        users = sesstion.query(model.Users).all()
        is_admin = False
        names = []
        # 全ユーザーの名前のリストを作成し管理者かどうかを確認する
        for user in users:
            names.append(user.name)
            # 通信したユーザーが管理者か確認する
            if user.id == user_id and user.admin: # JWTから取得したユーザーがDBに存在し管理者であるか確認
                is_admin = True
        # 管理者ならば全ユーザー名とユーザー数を返す
        if is_admin:
            return {"user_count": len(users), "user_names": names}
        else:
            return None

    # ユーザーの投稿と名前の情報を返す関数
    def get_user(self, user_id: int, session: Session) -> dict:
        p = []
        user = session.query(model.Users).filter(model.Users.id == user_id).first()
        pages = session.query(model.Pages).filter(model.Pages.user_id == user_id).all()
        points = session.query(model.Points).all()
        for page in pages:
            p.append(Page.convert_page(page=page, points=points))

        return {"name": user.name, "files": p}

    # ユーザーのパスワードを再設定する関数
    def put_user(self, user_id: int, user: model.ResponseUser, session: Session) -> bool:
        called_user = session.query(model.Users).filter(model.Users.id == user_id).first()

        # ユーザーが管理者かどうかを確認してから変更する
        try:
            if called_user.admin:
                temp = f"{user.name}{user.password}"
                password = hashlib.sha256(temp.encode("UTF-8")).hexdigest()

                # DBの値を更新する
                target_user = session.query(model.Users).filter(model.Users.name == user.name).first()
                target_user.password = password
                session.commit()
                return True
            else:
                return False
        except:
            session.rollback()
            return False
