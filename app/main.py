from fastapi import FastAPI
import json
import random

app = FastAPI()

@app.get("/")
def hello():
    return {"hello" : "Hello World"}

# 投稿したページをタグから検索して表示する
@app.get("/page")
def get_page():
    data = "./data.json"
    search ="./search.json"

    tag = "kankou"
    search_result = []
    result = dict()

    with open(search, mode="r", encoding="utf-8") as f:
        jn = json.loads(f.read())["tags"]
        num = jn[tag]["num"]
        file = jn[tag]["file"]

        rand = random.randint(0,num-1)
        search_result.append(file[rand])
        # for i in range(10):
        #     rand = random.randint(0,num-1)
        #     search_result.append(file[rand])

    with open(data, mode="r", encoding="utf-8") as f:
        d = json.loads(f.read())
        for i in file:
            result[i] = d[i]

    return result