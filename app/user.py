import datetime
import jwt
import hashlib
from database import DataBase

KEY = ""

# ユーザー情報のクラス
class User:

    def __init__(self):
        # ユーザーDBの接続
        self.db = DataBase()
        self.user_data = self.db.get_collection(collection_name="user_data")
        self.file_data = self.db.get_collection(collection_name="file_data")

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
    def regist(self, user):
        # ユーザー数の確認
        num = self.user_data.count_documents({})
        temp = f"{user.name}{user.password}"

        user_doc = {
            "id" : num + 1,
            "name" : user.name,
            "password" : hashlib.sha256(temp.encode("UTF-8")).hexdigest(),
            "checked" : []
        }

        # 同じ名前の人が存在するか確認
        find = self.user_data.find_one({"name" : user.name}, {"_id" : False})

        if (find):
            return {"token" : "exist name"}
        else:
            # DBにユーザーの情報を追加
            self.user_data.insert_one(user_doc)
            token= User.cleate_token(user_doc["id"])

            # 作成したユーザーのIDを返す
            return {"token" : token}

    # ユーザーがDBにあるか確認して存在すればIDを返却する
    def login(self, user):
        temp = f"{user.name}{user.password}"
        find = self.user_data.find_one({"$and":[{"name":user.name},{"password":hashlib.sha256(temp.encode("UTF-8")).hexdigest()}]}, {"_id": False})
        user_id = find["id"]
        token = User.cleate_token(user_id=user_id)

        return {"token" : token}

    # ユーザーの情報を返す
    def get_user(self, user_id):

        find = self.user_data.find_one({"id": user_id}, {"_id": False})
        files = self.file_data.find({"user":user_id}, {"_id":False})
        # 返せる情報のみを抜き出して返す
        user_doc = {
            "name" : find["name"],
            "checked" : find["checked"],
            "files" : list(files)
        }
        return user_doc

    def add_medal(self, user_id, shop_id):
        find = self.user_data.find_one({"id":user_id}, {"_id" : False})

        # すでにそのチェックポイントを巡回したか確認
        for checked_id in find["checked"]:
            if (checked_id == shop_id):
                return "error checked"
        
        # 追加
        self.user_data.update_one({"id":user_id}, {"$push": {"checked":shop_id}})
        return "success"