# search functions
from fuzzywuzzy import process, fuzz

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag


def search_by_term(user_query):
    """takes in brand string and returns list of product objects"""

    # getting all products for querying
    products_all = Product.query
    ingredients_all = Ingredient.query

    product_choices = []
    brand_choices_dup = []
    category_choices_dup = []
    ingredient_choices = []

    # create and dedupe lists of choices for fuzzy search to compare user query against
    product_aggregate_lookup = {}

    for product in products_all:
        # product_choices.append(product.pr_name)
        product_choices.append(product.pr_name +" "+ product.brand +" "+ product.category)
        product_aggregate_lookup[product.pr_name +" "+ product.brand +" "+ product.category] = product.pr_name
        brand_choices_dup.append(product.brand)
        category_choices_dup.append(product.category)
        brand_choices = list(set(brand_choices_dup))
        category_choices = list(set(category_choices_dup))
    for ingredient in ingredients_all:
        ingredient_choices.append(ingredient.ing_name)

    # get match scores
    # product_matches = process.extract(user_query, product_choices, scorer=fuzz.partial_ratio, limit = 20) 
    # product_matches = process.extract(user_query, product_choices, scorer=fuzz.ratio, limit = 20)
    product_matches = process.extract(user_query, product_choices, scorer=fuzz.partial_ratio, limit = 20)  
    brand_matches = process.extract(user_query, brand_choices, scorer=fuzz.partial_ratio, limit = 10) 
    category_matches = process.extract(user_query, category_choices, scorer=fuzz.partial_ratio) 
    ingredient_matches = process.extract(user_query, ingredient_choices, scorer=fuzz.ratio, limit = 15)

    # determine closest match
    product_match_score = product_matches[0][1]
    brand_match_score = brand_matches[0][1]
    category_match_score = category_matches[0][1]
    ingredient_match_score = ingredient_matches[0][1]

    match_scores_all = [(product_match_score, "product"), (brand_match_score, "brand"), (category_match_score, "category"), (ingredient_match_score, "ingredient")]
    sorted_match_scores_all = sorted(match_scores_all, key=lambda tup: tup[0])

    match_1 = sorted_match_scores_all[3][1]
    match_2 = sorted_match_scores_all[2][1]
    match_3 = sorted_match_scores_all[1][1]
    match_4 = sorted_match_scores_all[0][1]

    # create list of product objects
    products = []
    if product_matches:
        for product in product_matches:
            product_extract = product_aggregate_lookup[product[0]]
            prods = products_all.filter(Product.pr_name == product_extract).all()
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

    # create list of ingredients objects
    ingredients = []
    ingredient_names = []
    if ingredient_matches:
        for ingredient in ingredient_matches:
            ings = ingredients_all.filter(Ingredient.ing_name == ingredient[0]).all()
            for ing in ings:
                if ing not in ingredients:
                    ingredients.append(ing)
                    ingredient_names.append(ing.ing_name)

    # if there are objects in products list, return info for rendering, else return None to prompt error message
    if len(products) > 0:
        return (products, brands, categories, (match_1, match_2, match_3, match_4), ingredients, ingredient_names)

    else:
        return None


def return_close_ing_matches(user_flag_ings):
    """takes in ingredients for user custom flag and returns close matches"""

    ingredients_all = Ingredient.query

    ingredient_choices = []

    for ingredient in ingredients_all:
        ingredient_choices.append(ingredient.ing_name)

    auto_add_ing = []
    confirm_add_ing = []

    # get match scores
    for ing in user_flag_ings:
        split_ing = ing.split()
        if len(split_ing) > 1:
            ingredient_matches = process.extract(ing, ingredient_choices, scorer=fuzz.ratio)
        else:
            ingredient_matches = process.extract(ing, ingredient_choices, scorer=fuzz.partial_ratio)
        for fuzz_ing in ingredient_matches:
            if fuzz_ing[1] >= 99:
                auto_add_ing.append(fuzz_ing[0])
            elif fuzz_ing[1] >= 85:
                confirm_add_ing.append(fuzz_ing[0])

    # if there are objects in either list, return those matches, else return None to prompt error message
    return (auto_add_ing, confirm_add_ing)






























