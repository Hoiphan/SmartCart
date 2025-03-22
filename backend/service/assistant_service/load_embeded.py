import json
import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

#Load the .env file
load_dotenv()

with open("../../resources/products.json", "r", encoding="utf-8") as file:
    products = json.load(file)

# Operating pinecon
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Create index-name
index_name = os.getenv("INDEX_NAME")

# Get the list of index names
index_names = [index['name'] for index in pc.list_indexes()]

# Check if the index exists
if index_name in index_names:
    print(f"Index '{index_name}' already exists. Choose a different name or delete the existing index.")
    # You can choose to delete the existing index using:
    # pc.delete_index(index_name)
else:
    pc.create_index(
        name=index_name,
        dimension=1024, # Replace with your model dimensions
        metric="cosine", # Replace with your model metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"Index '{index_name}' created successfully.")


# Format text before embedding 
def format_product(product):
    return f"""
    Tên sản phẩm: {product['product_name']}.
    Mô tả: {product['description']}.
    Giá: {product['price']} VND.
    Danh mục: {product['category']}.
    Thương hiệu: {product['brand']}.
    Xuất xứ: {product['origin']}.
    Hạn sử dụng: {product['expiry_date']}.
    Ngày sản xuất: {product['manufacture_date']}.
    Dung tích/KL: {product['volume']}.
    Số lượng tồn kho: {product['stock']}.
    Đánh giá trung bình: {product['rating']}.
    Bình luận: {', '.join([r['comment'] for r in product['reviews']])}.
    """

# Chuyển toàn bộ danh sách sản phẩm thành văn bản embedding
text_list = [format_product(p) for p in products]

embeddings = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=text_list,
    parameters={"input_type": "passage", "truncate": "END"}
)

# Print  first embeded vector nn a trial basis
print(embeddings[0])

# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

# Call Index Object
index = pc.Index(index_name)

# Create vector
vectors = [
    (
        str(p["product_id"]),
        emb['values'],
        {
            "product_name": p["product_name"],
            "description": p["description"],
            "price": p["price"],
            "category": p["category"],
            "brand": p["brand"],
            "rating": p["rating"],
            "nutrition": str(p["nutrition_facts"])
        }
    )
    for p, emb in zip(products, embeddings)
]


# Officialy embed the matrix
index.upsert(
    vectors=vectors,
    namespace="ns1"
)

# Print meta data
print(index.describe_index_stats())

