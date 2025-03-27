import json
import os
class PromotionRecommendationService:
    def __init__(self):
        self.promotions = self.load_promotions()
    
    def load_promotions(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "..", "resources", "promotion.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def recommend_promotion(self, current_cart) -> list:
        # Using basic search algorithm
        recommended_promotions = []

        for item in current_cart:
            product_id = item.get("product_id")

            for promo in self.promotions:
                if promo["product_id"] == product_id:
                    recommended_promotions.append({
                        "product_id": product_id,
                        "product_name": item.get("product_name", "Unknown Product"),
                        "description": promo["description"],
                        "image": promo["image"]
                    })
        
        return recommended_promotions
    
def promotion_recommendation(current_cart):
    promotion_service = PromotionRecommendationService()
    return promotion_service.recommend_promotion(current_cart)