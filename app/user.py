from database import DataBase

# ユーザー情報のクラス
class User:

    def __init__(self):
        # ユーザーDBの接続
        self.db = DataBase()
        self.user_data = self.db.get_collection(collection_name="user_data")

    # ユーザーの情報を追加
    def post_user(self, user):
        # ユーザー数の確認
        num = self.user_data.count_documents({})

        user_doc = {
            "user_id" : num + 1,
            "user_name" : user.name,
            "password" : user.password,
            "checked" : []
        }

        # DBにユーザーの情報を追加
        self.user_data.insert_one(user_doc)

        # 作成したユーザーのIDを返す
        return {"user_id" : num + 1}

    # ユーザーの情報を返す
    def get_user(self, user_id):
        find = self.user_data.find_one({"user_id": user_id}, {"_id": False})

        # 返せる情報のみを抜き出して返す
        user_doc = {
            "user_name" : find["user_name"],
            "checked" : find["checked"]
        }

        return user_doc