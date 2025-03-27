import sys
import os

# Add the 'service' folder to the system path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), 'service'))

# Import the ProductSearching class from the product_searching_service module
from product_searching_service import ProductSearching
from promotion_recommendation_service import PromotionRecommendationService

def main():
    # Create an instance of the ProductSearching class
    product_search = ProductSearching()
    
    # Test input string (you can modify this for different searches)
    user_input = input("Enter product name to search: ")
    
    # Get the closest products based on the input string
    closest_products = product_search.search(user_input)
    
    # Display the closest products
    if closest_products:
        print(f"Top {len(closest_products)} closest products to '{user_input}':")
        for product in closest_products:
            print(f"Product Name: {product['product_name']}")
            print(f"Price: {product['price']}")
            print(f"Description: {product['description']}")
            print(f"Rating: {product['rating']}")
            print("-" * 40)
    else:
        print("No products found.")
        
    current_cart = [
        {"product_id": 1, "product_name": "Diary Milk", "price": "49000"},
        {"product_id": 2, "product_name": "TH Milk", "price": "50000"}
    ]

    promo_service = PromotionRecommendationService()
    promotions = promo_service.recommend_promotion(current_cart)

    if promotions:
        print("🎉 Promotions Found:")
        for promo in promotions:
            print(f"🔹 {promo['product_name']}: {promo['description']}")
    else:
        print("❌ No promotions available.")


if __name__ == "__main__":
    main()