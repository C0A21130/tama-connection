from pydantic import BaseModel

class Location(BaseModel):
    x: float
    y: float

# put_page関数の受け取るjsonデータの型
class Page(BaseModel):
    title: str
    tag: str
    text: str
    location_name : str
    location: Location
    image: str

# post_user関数の受け取るjsonデータの型
class User(BaseModel):
    name: str
    password: str

# add_medal関数の受け取るjsonデータの型
class Shop(BaseModel):
    shop_id: int