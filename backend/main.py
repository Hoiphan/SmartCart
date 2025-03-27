from service.product_recommendation_service import ProductRecommendationService

if __name__ == '__main__':
    prs = ProductRecommendationService()
    print(prs.recommend_next_product([1, 2]))