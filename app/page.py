from database import DataBase

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
    def get_page(self):
        search_result = {"kankou": [], "gurume": [], "tamasanpo":[], "omiyage":[]}

        tags  = ["kankou", "gurume", "tamasanpo" ,"omiyage"]
        page_names:dict = {"kankou": [], "gurume": [], "tamasanpo":[], "omiyage":[]}

        # 該当するタグのページの名前をDBから検索する
        for tag in tags:
            finds = self.file_data.find({"tag" : tag}, {"_id": False})
            for find in list(finds):
                page_names[tag].append(find["file_name"])

        # 検索されたページの名前から該当するページのデータをDBから取得する
        for tag in page_names:
            for page_name in page_names[tag]:
                page_data =  Page.get_one_page(page_id=page_name)
                search_result[tag].append(page_data)

        return search_result

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
        result = self.file_data.insert_one(new_page)

        return next_files_num