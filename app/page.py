from database import DataBase

PAGES_NUM = 3

class Page:

    @classmethod
    def get_one_page(cls, page_id):
        # DBと接続する
        db = DataBase()
        file_data = db.get_collection(collection_name="file_data")

        # 指定したページ番号から情報を取得する
        search_result: dict = file_data.find_one({"file_name" : page_id}, {"_id" : False})

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
            return {"result":kankou[start_index : start_index+PAGES_NUM], "max":max_page}
        elif (tag == "gurume"):
            return {"result":gurume[start_index : start_index+PAGES_NUM], "max":max_page}
        elif (tag == "tamasanpo"):
            return {"result":tamasanpo[start_index : start_index+PAGES_NUM], "max":max_page}
        else:
            return {"result":omiyage[start_index : start_index+PAGES_NUM], "max":max_page}

    # ページの投稿
    def post_page(self, page, user_id: int):
        # DBからデータ数を読み取る
        finds_num:int = self.file_data.count_documents({})
        
        # 新しいページ番号の作成
        next_files_num: int = finds_num + 1

        # 受けとったjsonデータから新しいページを作成する
        new_page = {
            "file_name": next_files_num,
            "title": page.title,
            "tag": page.tag,
            "text": page.text,
            "user": user_id,
            "location": {
                "x": page.location.x,
                "y": page.location.y
            },
            "image" : page.image
        }

        # 新しく作成したデータをDBに追加
        self.file_data.insert_one(new_page)

        return next_files_num