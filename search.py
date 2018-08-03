# search functions
from fuzzywuzzy import process, fuzz

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, Category



def search_by_ingredient(user_ingredient_search):
    """takes in ingredient string and returns list of product objects"""

    ingredients = Ingredient.query.all()
    choices = []
    for ingredient in ingredients:
        choices.append(ingredient.ing_name)
    # fuzzy search with a cutoff score of 85
    match = process.extractOne(user_ingredient_search, choices, scorer=fuzz.ratio, score_cutoff = 85) 
    if match:
        ingredient = Ingredient.query.filter_by(ing_name=match[0]).first()
        return ingredient.ing_products
    else:
        return None


def search_by_brand(user_brand_search):
    """takes in brand string and returns list of product objects"""

    products = Product.query.all()
    choices = []
    for product in products:
        choices.append(product.brand)
    # fuzzy search with a cutoff score of 95
    match = process.extractOne(user_brand_search, choices, scorer=fuzz.ratio, score_cutoff = 75) 
    if match:
        return Product.query.filter_by(brand=match[0]).all()
    else:
        return None


def search_by_product(user_product_search):
    """takes in product name string and returns list with single product"""

    products = Product.query.all()
    choices = []
    for product in products:
        choices.append(product.pr_name)
    # fuzzy search with a cutoff score of 90
    match = process.extractOne(user_product_search, choices, scorer=fuzz.ratio, score_cutoff = 75)  
    if match:
        return Product.query.filter_by(pr_name=match[0]).all()
    else:
        return None


def search_by_ingredient_and_brand(user_ingredient_search, user_brand_search):
    """takes in ingredient string and brand string and returns list of product objects"""

    
    ingredient_choices = Ingredient.query(ing_name).all()
    brand_choices = Product.query(brand).all()

    ingredients = Ingredient.query.all()
    ingredient_choices = []
    for ingredient in ingredients:
        ingredient_choices.append(ingredient.ing_name)

    products = Product.query.all()
    brand_choices = []
    for product in products:
        brand_choices.append(product.brand)
    
    # fuzzy ingredient search with a cutoff score of 90
    ingredient_match = process.extractOne(user_ingredient_search, ingredient_choices, scorer=fuzz.ratio, score_cutoff = 85) 
    if ingredient_match:
        ingredient = Ingredient.query.filter_by(ing_name=match).first()
        ingredient_products = ingredient.ing_products
        # fuzzy ingredient search with a cutoff score of 95
        brand_match = process.extractOne(user_brand_search, brand_choices, scorer=fuzz.ratio, score_cutoff = 75) 
        if brand_match:
            brand_ingredient_match_products = []
            for product in ingredient_products:
                if product.brand == brand_match:
                    brand_ingredient_match_products.append(product)
            return brand_ingredient_match_products

    return None



