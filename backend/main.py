from fastapi import Body, FastAPI
from pydantic import BaseModel
from fastapi import Request



##import assistant
from service.assistant_service.func_prompt import res_gemini
from service.product_recommendation_service import product_searching
from service.product_searching_service import promotion_recommendation


app = FastAPI()


class Item(BaseModel):
    name: str
    des: str = None
    price: float
    tax: float = None


# Request model (optional but recommended)
class TextInput(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str
    
class CartRequest(BaseModel):
    current_cart: list[Item]  

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

@app.post("/search/")
def search_products(request: SearchRequest):
    results = product_searching(request.query)
    return {"results": results}

@app.post("/recommend_promotion/")
def recommend_promotion(request: CartRequest):
    results = promotion_recommendation(request.current_cart)
    return {"recommended_promotions": results}