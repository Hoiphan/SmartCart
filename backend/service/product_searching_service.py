# Levenshtein distance
import json
import os
from Levenshtein import distance

class ProductSearching:
    def __init__(self):
        self.products = self.load_products()
        
    def load_products(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "..", "resources", "products.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search(self, input) -> list:
        # Using Levenshtein distance
        distances = []
        
        for product in self.products:
            product_name = product['product_name']
            lev_distance = distance(input.lower(), product_name.lower())
            max_len = max(len(input), len(product_name))
            similarity = 1 - (lev_distance / max_len)
            distances.append((product, similarity))
            
        distances.sort(key=lambda x: x[1], reverse=True)
        
        return [item[0] for item in distances[:5]]
    
def product_searching(input):
    product_service = ProductSearching()
    return product_service.search(input)