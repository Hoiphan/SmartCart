import json

# FP-Growth
# Content-based Recommendation System
# Markov Chain
# MLP

# Minh

import os
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from pathlib import Path

class ProductRecommendationService:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        file_path = self.base_dir / '..' / 'resources' / 'products.json'

        self.products = self.read_json_file(str(file_path))
        # self.products = self.read_json_file('resources/products.json')
        self.product_ids_list = self.get_product_ids_list(self.products)
        self.receipt_ids_list = self.get_receipt_ids_list()
        self.receipt_product_matrix = self.build_receipt_product_matrix(self.receipt_ids_list, self.product_ids_list)
        self.association_rules = self.build_association_rule(self.receipt_product_matrix, self.product_ids_list)

    def read_json_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    def get_product_ids_list(self, products):
        return list(map(lambda p: p['product_id'], products))
    
    def get_receipt_ids_list(self):
        dir_path = self.base_dir / '..' / 'resources' / 'receipts'
        return list(map(lambda f: f.split('.')[0], os.listdir(str(dir_path))))
    
    def build_receipt_product_matrix(self, receipt_ids_list, product_ids_list):
        matrix = np.zeros((len(receipt_ids_list), len(product_ids_list)))
        for receipt_id in receipt_ids_list:
            file_path = self.base_dir / '..' / 'resources' / 'receipts' / f'{receipt_id}.json'
            receipt = self.read_json_file(str(file_path))
            for product in receipt['products']:
                if product['product_id']:
                    matrix[int(receipt_id) - 1, product['product_id'] - 1] = 1

        return matrix
    
    def build_association_rule(self, matrix, product_ids_list):
        data = pd.DataFrame(matrix, columns=product_ids_list)
        data = data.astype(bool)
        frequent_itemsets = fpgrowth(data, min_support=0.4, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6, num_itemsets=len(frequent_itemsets))
        return rules

    def recommend_next_product(self, cart, top_n=3) -> int:
        recommendations = {}

        # Duyệt qua từng luật để tìm luật phù hợp với giỏ hàng
        for _, row in self.association_rules.iterrows():
            antecedent = set(row['antecedents'])
            consequent = set(row['consequents'])
            confidence = row['confidence']

            # Nếu giỏ hàng chứa toàn bộ antecedent của luật
            if antecedent.issubset(cart):
                for item in consequent:
                    if item not in cart:  # Chỉ đề xuất sản phẩm chưa có trong giỏ
                        if item in recommendations:
                            recommendations[item] = max(recommendations[item], confidence)
                        else:
                            recommendations[item] = confidence

        # Sắp xếp sản phẩm theo độ tin cậy
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

        # Trả về danh sách top_n sản phẩm gợi ý
        return [item for item, _ in sorted_recommendations[:top_n]]

if __name__ == '__main__':
    prs = ProductRecommendationService()
    print(prs.product_ids_list)