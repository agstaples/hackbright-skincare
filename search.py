# search functions
from fuzzywuzzy import process, fuzz

from model import Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, Category
from flask import session


def search_by_ingredient():
    """takes in ingredient string and returns list of product objects"""

    user_ingredient_search = session["ingredient_search"]
    choices = Ingredient.query(ing_name_lower).all()
    # fuzzy search with a cutoff score of 85
    match = process.extractOne(user_ingredient_search, choices, scorer=fuzz.ratio, score_cutoff = 90) 
    if match:
        ingredient = Ingredient.query.filter_by(ing_name_lower=match).first()
        return ingredient.ing_products
    else:
        return None


def search_by_brand():
    """takes in brand string and returns list of product objects"""

    user_brand_search = session["brand_search"]
    choices = Product.query(brand).all()
    # fuzzy search with a cutoff score of 95
    match = process.extractOne(user_brand_search, choices, scorer=fuzz.ratio, score_cutoff = 95) 
    if match:
        return Product.query.filter_by(brand_lower=match).all()
    else:
        return None


def search_by_product():
    """takes in product name string and returns list with single product"""

    user_product_search = session["product_search"]
    choices = Product.query(pr_name_lower).all()
    # fuzzy search with a cutoff score of 90
    match = process.extractOne(user_product_search, choices, scorer=fuzz.ratio, score_cutoff = 90)  
    if match:
        return [match]
    else:
        return None


def search_by_ingredient_and_brand():
    """takes in ingredient string and brand string and returns list of product objects"""

    user_ingredient_search = session["ingredient_search"]
    user_brand_search = session["brand_search"]
    
    ingredient_choices = Ingredient.query(ing_name_lower).all()
    brand_choices = choices = Product.query(brand).all()
    
    # fuzzy ingredient search with a cutoff score of 90
    ingredient_match = process.extractOne(user_ingredient_search, choices, scorer=fuzz.ratio, score_cutoff = 90) 
    if ingredient_match:
        ingredient = Ingredient.query.filter_by(ing_name_lower=match).first()
        ingredient_products = ingredient.ing_products
        # fuzzy ingredient search with a cutoff score of 95
        brand_match = process.extractOne(user_brand_search, choices, scorer=fuzz.ratio, score_cutoff = 95) 
        if brand_match:
            brand_ingredient_match_products = []
            for product in ingredient_products:
                if product.brand == brand_match:
                    brand_ingredient_match_products.append(product)
            return brand_ingredient_match_products

    return None

