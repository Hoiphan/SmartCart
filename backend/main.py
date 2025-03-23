from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    des: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_items(items: Item):
    return {"item_name": items.name, "item_price": items.price}


@app.get("/")
def read_root():
    return {"message": "Hello, World"}

@app.get("/item/{items_id}")
def read_item(items_id: int, q: str = 'Hello'):
    return {'item': items_id, "q": q}
    