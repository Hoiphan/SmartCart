import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from google import genai


#load env
load_dotenv()

# Operating pinecon
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Create index-name
index_name = os.getenv("INDEX_NAME")

# Call Index Object
index = pc.Index(index_name)

# Function to get embedded vectorbase based on query
def get_answer(query, top_k = 3):
    """Embeds the query, searches the index, and prints the top result."""

    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={"input_type": "query"}
    )
    results = index.query(

    vector=embedding[0].values,
    namespace="ns1",
    top_k=top_k,
    include_values=False,
    include_metadata=True
    )

    # Lists of product that must return
    products = []

    if results['matches']:
        for match in results['matches']:
            product = match['metadata']
            products.append(product)
    else:
        return None
    return products



## Create prompt completely to require genini
def ask_gemini(question):
    """Tìm sản phẩm liên quan và hỏi Gemini AI"""
    related_products = get_answer(question)

    if not related_products:
        return "Xin lỗi, tôi không tìm thấy sản phẩm nào phù hợp."

    product_info = "\n".join([
        str(p)
        for p in related_products
    ])

    prompt = f"""Bạn là một chuyên gia tư vấn sản phẩm. Người dùng hỏi: "{question}".
    Đây là danh sách sản phẩm liên quan:
    {product_info}

    Dựa vào thông tin trên, hãy trả lời một cách ngắn gọn và tự nhiên.
    """

    return prompt

# Asking gemini in reality
client = genai.Client(api_key=os.getenv('GEMINI_KEY'))

def res_gemini(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=ask_gemini(prompt),
    )

    return response.text