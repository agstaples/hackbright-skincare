# search functions
from fuzzywuzzy import process, fuzz

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag


def search_by_term(user_query):
    """takes in brand string and returns list of product objects"""

    products_all = Product.query

    product_choices = []
    brand_choices = []
    category_choices = []

    for product in products_all:
        product_choices.append(product.pr_name)
        brand_choices.append(product.brand)
        category_choices.append(product.category)

    product_matches = process.extract(user_query, product_choices, scorer=fuzz.partial_ratio, limit = 40) 
    brand_matches = process.extract(user_query, brand_choices, scorer=fuzz.partial_ratio, limit = 10) 
    category_matches = process.extract(user_query, category_choices, scorer=fuzz.partial_ratio, limit = 5) 

    # determine closest match
    product_match_score = product_matches[0][1]
    brand_match_score = brand_matches[0][1]
    category_match_score = category_matches[0][1]

    highest_match = "product"
    if category_match_score >= brand_match_score:
        if category_match_score >= product_match_score:
            highest_match = "category"
        else:
            highest_match = "product"
    elif brand_match_score >= category_match_score:
        if brand_match_score >= product_match_score:
            highest_match = "brand"
        else:
            highest_match = "product"

    products = []
    product_names = []
    if product_matches:
        for product in product_matches:
            products.append(products_all.filter(Product.pr_name == product[0]).all())

    brands = []
    if brand_matches:
        for brand in brand_matches:
            products.append(products_all.filter(Product.brand == brand[0]).all())
            brands.append(brand[0])

    categories = []
    if category_matches:
        for category in category_matches:
            products.append(products_all.filter(Product.category == category[0]).all())
            categories.append(category[0])

    if len(products) > 0:
        products_return = list(set([product for product_list in products for product in product_list]))
        return (products_return, brands, categories, highest_match)

    else:
        return None





































