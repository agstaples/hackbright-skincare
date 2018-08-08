# search functions
from fuzzywuzzy import process, fuzz

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag


def search_by_term(user_query):
    """takes in brand string and returns list of product objects"""

    products_all = Product.query

    product_choices = []
    brand_choices_dup = []
    category_choices_dup = []

    for product in products_all:
        product_choices.append(product.pr_name)
        brand_choices_dup.append(product.brand)
        category_choices_dup.append(product.category)
        brand_choices = list(set(brand_choices_dup))
        category_choices = list(set(category_choices_dup))

    product_matches = process.extract(user_query, product_choices, scorer=fuzz.partial_ratio, limit = 20) 
    brand_matches = process.extract(user_query, brand_choices, scorer=fuzz.partial_ratio, limit = 5) 
    category_matches = process.extract(user_query, category_choices, scorer=fuzz.partial_ratio, limit = 3) 

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
    if product_matches:
        for product in product_matches:
            prods = products_all.filter(Product.pr_name == product[0]).all()
            for prod in prods:
                products.append(prod)

    brands = []
    brand_products = []
    if brand_matches:
        for brand in brand_matches:
            brands.append(brand[0])
            brand_prods = products_all.filter(Product.brand == brand[0]).limit(10).all()
            for brand_prod in brand_prods:
                brand_products.append(brand_prod)

    categories = []
    category_products = []
    if category_matches:
        for category in category_matches:
            categories.append(category[0])
            cat_prods = products_all.filter(Product.category == category[0]).limit(10).all()
            for cat_prod in cat_prods:
                category_products.append(cat_prod)

    products_return = []

    if highest_match == "product":
        for product in products:
            if product not in products_return:
                products_return.append(product)
        for product in brand_products:
            if product not in products_return:
                products_return.append(product)
        for product in category_products:
            if product not in products_return:
                products_return.append(product)

    elif highest_match == "brand":
        for product in brand_products:
            if product not in products_return:
                products_return.append(product)
        for product in products:
            if product not in products_return:
                products_return.append(product)
        for product in category_products:
            if product not in products_return:
                products_return.append(product)

    elif highest_match == "category":
        for product in category_products:
            if product not in products_return:
                products_return.append(product)
        for product in products:
            if product not in products_return:
                products_return.append(product)
        for product in brand_products:
            if product not in products_return:
                products_return.append(product)


    if len(products) > 0:
        return (products_return, brands, categories, highest_match, product_match_score, brand_match_score, category_match_score)

    else:
        return None





































