from fastapi import Body, FastAPI
from pydantic import BaseModel
from fastapi import Request



##import assistant
from service.assistant_service.func_prompt import res_gemini


app = FastAPI()


class Item(BaseModel):
    name: str
    des: str = None
    price: float
    tax: float = None


# Request model (optional but recommended)
class TextInput(BaseModel):
    text: str

@app.post("/items/")
def create_items(items: Item):
    return {"item_name": items.name, "item_price": items.price}


@app.get("/")
def read_root():
    return {"message": "Hello, World"}

@app.get("/item/{items_id}")
def read_item(items_id: int, q: str = 'Hello'):
    return {'item': items_id, "q": q}

@app.post("/assist")
def ask_gemini(
    text: str = Body(..., media_type="text/plain")  # ← Accepts raw text
):
    text_gemini = res_gemini(text)
    
    return {"response": f"{text_gemini}"}  # Return as plain text or JSON