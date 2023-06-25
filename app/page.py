from database import DataBase

PAGES_NUM = 3

class Page:

    @classmethod
    def get_one_page(cls, page_id: int, user_id):
        # DBと接続する
        db = DataBase()
        file_data = db.get_collection(collection_name="file_data")
        user_status = []

        # 指定したページ番号から情報を取得する
        search_result: dict = file_data.find_one({"page_id" : page_id}, {"_id" : False})
        # ユーザーがアカウント登録しているかを確認する
        for status in ["good", "went", "go"]: 
            # ユーザーが既にいいねをしていたかを確認する
            for i in search_result[status]:
                if i == user_id:
                    user_status.append(status)
        search_result["user_status"] = user_status
        # ユーザーIDからユーザー数に変換
        for status in ["good", "went", "go"]:
            search_result[status] = len(search_result[status])

        return search_result

    def __init__(self):
        self.db = DataBase()
        self.file_data = self.db.get_collection(collection_name="file_data")
    
    # 複数ページを取得する
    def get_pages(self, tag, page_num):
        # リストの初期化
        kankou = list()
        gurume = list()
        tamasanpo = list()
        omiyage = list()

        # 取得したデータを分類する
        for doc in list(self.file_data.find({},{"_id":False})):
            # ユーザーIDからユーザー数に変換
            for status in ["good", "went", "go"]:
                doc[status] = len(doc[status])

            if (doc["tag"] == "kankou"):
                kankou.append(doc)
            elif (doc["tag"] == "gurume"):
                gurume.append(doc)
            elif (doc["tag"] == "tamasanpo"):
                tamasanpo.append(doc)
            else:
                omiyage.append(doc)

        # 数を数える
        max_page = {
            "kankou": len(kankou), 
            "gurume": len(gurume),
            "tamasanpo": len(tamasanpo),
            "omiyage": len(omiyage),
        }

        # 取得する範囲の最初を決める
        start_index = PAGES_NUM * page_num

        # 結果を返却する
        if (tag == "kankou"):
            kankou.reverse()
            return {"result":kankou[start_index : start_index+PAGES_NUM], "max":max_page}
        elif (tag == "gurume"):
            gurume.reverse()
            return {"result":gurume[start_index : start_index+PAGES_NUM], "max":max_page}
        elif (tag == "tamasanpo"):
            tamasanpo.reverse()
            return {"result":tamasanpo[start_index : start_index+PAGES_NUM], "max":max_page}
        else:
            omiyage.reverse()
            return {"result":omiyage[start_index : start_index+PAGES_NUM], "max":max_page}

    # ページの投稿
    def post_page(self, page, user_id: int):
        # DBからファイル名の最大値を読み取る
        docs = list(self.file_data.find({}, {"_id":False}).sort("page_id", -1))

        # 受けとったjsonデータから新しいページを作成する
        new_page = {
            "page_id": docs[0]["page_id"] + 1,
            "title": page.title,
            "tag": page.tag,
            "text": page.text,
            "user": user_id,
            "location_name": page.location_name,
            "location": {
                "x": page.location.x,
                "y": page.location.y
            },
            "image" : page.image,
            "good": [],
            "went": [],
            "go": []
        }

        # 新しく作成したデータをDBに追加
        self.file_data.insert_one(new_page)

        return docs[0]["page_id"] + 1

    # 投稿したページの変更
    def put_page(self, page_id, page, user_id):
        update_page = {
            "page_id": page_id,
            "title": page.title,
            "tag": page.tag,
            "text": page.text,
            "user": user_id,
            "location": {
                "x": page.location.x,
                "y": page.location.y
            },
            "image": page.image
        }
        self.file_data.replace_one({"page_id":page_id}, update_page)
        return page_id

    # ページの削除
    def delete_page(self, page_id):
        self.file_data.delete_one({"page_id": page_id})
        return page_id
