# search functions
from fuzzywuzzy import process, fuzz

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag


def search_by_term(user_query):
    """takes in brand string and returns list of product objects"""

    # getting all products for querying
    products_all = Product.query

    product_choices = []
    brand_choices_dup = []
    category_choices_dup = []

    # create and dedupe lists of choices for fuzzy search to compare user query against
    for product in products_all:
        product_choices.append(product.pr_name)
        brand_choices_dup.append(product.brand)
        category_choices_dup.append(product.category)
        brand_choices = list(set(brand_choices_dup))
        category_choices = list(set(category_choices_dup))

    # get match scores
    product_matches = process.extract(user_query, product_choices, scorer=fuzz.partial_ratio, limit = 20) 
    brand_matches = process.extract(user_query, brand_choices, scorer=fuzz.partial_ratio, limit = 10) 
    category_matches = process.extract(user_query, category_choices, scorer=fuzz.partial_ratio) 

    # determine closest match
    product_match_score = product_matches[0][1]
    brand_match_score = brand_matches[0][1]
    category_match_score = category_matches[0][1]

    match_1 = "product"
    match_2 = "brand"
    match_3 = "category"

    if category_match_score >= brand_match_score and category_match_score >= product_match_score:
        match_1 = "category"
        if brand_match_score >= product_match_score:
            match_2 = "brand"
            match_3 = "product"
        else:
            match_2 = "product"
            match_3 = "brand"
    elif brand_match_score >= category_match_score and brand_match_score >= product_match_score:
        match_1 = "brand"
        if category_match_score >= product_match_score:
            match_2 = "category"
            match_3 = "product"
        else:
            match_2 = "product"
            match_3 = "category"

    # create list of product objects
    products = []
    if product_matches:
        for product in product_matches:
            prods = products_all.filter(Product.pr_name == product[0]).all()
            for prod in prods:
                if prod not in products:
                    products.append(prod)

    # create list of brands
    brands = []
    if brand_matches:
        for brand in brand_matches:
            brands.append(brand[0])

    # create list of categories
    categories = []
    if category_matches:
        for category in category_matches:
            categories.append(category[0])

    # if there are objects in products list, return info for rendering, else return None to prompt error message
    if len(products) > 0:
        return (products, brands, categories, (match_1, match_2, match_3), product_match_score, brand_match_score, category_match_score)

    else:
        return None





































