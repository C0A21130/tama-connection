from pydantic import BaseModel

class Location(BaseModel):
    x: float
    y: float

class Other(BaseModel):
    user: str
    location: Location

# put_page関数の受け取るjsonデータの型
class Page(BaseModel):
    title: str
    tag: str
    text: str
    other: Other