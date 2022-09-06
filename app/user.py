import os
import datetime
from database import DataBase
import jwt

KEY = os.environ["KEY"]

# ユーザー情報のクラス
class User:

    def __init__(self):
        # ユーザーDBの接続
        self.db = DataBase()
        self.user_data = self.db.get_collection(collection_name="user_data")

    # JWTのトークンを生成する
    @classmethod
    def cleate_token(cls, user_id):
        dt_now = datetime.datetime.now()
        td_1d = datetime.timedelta(days=10)
        exp = dt_now + td_1d

        payload = {
            "id" : user_id,
            "exp" : exp.strftime("%Y-%m-%d %H:%M")
        }
        result = jwt.encode(payload, KEY, algorithm="HS256")
        return result

    @classmethod
    def get_id(cls, token):
        # JWTの期限を確認する
        data = jwt.decode(token, KEY, algorithm="HS256")
        data_exp = datetime.datetime.strptime(data["exp"], "%Y-%m-%d %H:%M")
        dt_now = datetime.datetime.now()
        if (dt_now < data_exp):
            return "exp error"
        
        # ユーザーID
        user_id = data["id"]
        return user_id

    # ユーザーの情報を追加
    def post_user(self, user):
        # ユーザー数の確認
        num = self.user_data.count_documents({})

        user_doc = {
            "id" : num + 1,
            "name" : user.name,
            "password" : user.password,
            "checked" : []
        }

        # 同じ名前の人が存在するか確認
        find = self.user_data.find_one({"name" : user.name}, {"_id" : False})

        if (find):
            return {"user_id" : "exist name"}
        else:
            # DBにユーザーの情報を追加
            self.user_data.insert_one(user_doc)

            # 作成したユーザーのIDを返す
            return {"user_id" : user_doc["id"]}

    # ユーザーがDBにあるか確認して存在すればIDを返却する
    def login(self, user):
        find = self.user_data.find_one({"$and":[{"name":user.name},{"password":user.password}]}, {"_id": False})
        user_id = find["id"]
        token = User.cleate_token(user_id=user_id)

        return {"token" : token}

    # ユーザーの情報を返す
    def get_user(self, token):
        user_id = User.get_id(token=token)

        find = self.user_data.find_one({"id": user_id}, {"_id": False})

        # 返せる情報のみを抜き出して返す
        user_doc = {
            "name" : find["name"],
            "checked" : find["checked"]
        }

        return user_doc