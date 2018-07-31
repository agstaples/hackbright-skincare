"""Seeds skincare database from csv and txt files"""

from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from sqlalchemy import func
from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, Category
from server import app
import os
# from sephora_scrape import scrape_relevant_product_info

def load_products(doc="seed_data/valid_skin_urls.txt"):
    """Loads product data from Sephora scrape"""

    counter = 0

    # getting already vetted urls from file
    with open(doc) as valid_skin_urls:
        urls = valid_skin_urls.readlines()
        for url in urls:
            counter += 1
            url = str(url.rstrip())
            # providing headers for client, otherwise request fails
            header = {"User-Agent":"Firefox"}
            request = Request(url, headers=header)
            page = urlopen(request)
            # creating BeautifulSoup object for parsing
            soup = BeautifulSoup(page, "html.parser")
            # getting product name
            name = soup.find(attrs={"class": "css-1g2jq23"}).string
            if name:
                # getting product brand
                brand = soup.find(attrs={"class": "css-cjz2sh"}).string
                # getting star rating as percentage
                stars_object = soup.find(attrs={"class": "css-dtomnp"})
                stars = str(stars_object["style"].strip("%").split(":")[-1])
                # getting price from sephora page
                price_string = soup.find(attrs={"class": "css-18suhml"}).string
                if price_string == None:
                    price = str(0)
                else:
                    price = str(price_string.strip("$"))
                # product box contains all product information inculding ingredients
                product_box = soup.find_all(attrs={'class': 'css-1juot2r'})
                ingredients_all = product_box[-1].text
                ingredients_list = ingredients_all.split("\n")
                if len(ingredients_list[-1]) < 1:
                    ingredients = ingredients_list[-2].rstrip(".")
                else:
                    ingredients = ingredients_list[-1].rstrip(".")
                # creating product instance
                product = Product(sephora_url=url, 
                          pr_name=name, 
                          pr_name_lower=name.lower(), 
                          brand=brand, 
                          brand_lower=brand.lower(),
                          stars=float(stars), 
                          price=float(price),
                          ingredients=ingredients)
                db.session.add(product)
            else:
                print("***ERROR***")
                print(url)
                return
    db.session.commit()


def create_product_ingredient_dictionary():
    """created dictionary or product ingredients to populate ingredient and product_ingredient tables"""

    prod_ing_dict = {}

    
    products = Product.query.all()
    for product in products:
        product_id = product.product_id
        # adding product_id keys to dictionary
        prod_ing_dict[product_id] = []
        # getting list of ingredients for each product
        ingredients_all = product.ingredients.split(",")
        for ingredient_single in ingredients_all:
            # cleaning up individual ingredientt and adding as values to dictionary
            ingredient_single = ingredient_single.strip(" ").rstrip(".\n").rstrip(".\r")
            prod_ing_dict[product_id].append(ingredient_single.lower())

    return prod_ing_dict


def load_ingredients():
    """Loads ingredient data"""

    prod_ing_dict = create_product_ingredient_dictionary()
    ingredient_list = []

    for key, value in prod_ing_dict.items():
        for ingredient in value:
            ingredient_list.append(ingredient)

    # making list of unique ingredients
    ingredient_list = list(set(ingredient_list))

    for ingredient in ingredient_list:
        # creating ingredient instance
        ingredient = Ingredient(ing_name=ingredient, 
                                ing_name_lower=ingredient.lower())

        db.session.add(ingredient)

    db.session.commit()


def load_product_ingredients():
    """Loads product/ingredient data"""

    prod_ing_dict = create_product_ingredient_dictionary()

    # getting full list of unique ingredients
    ingredients = Ingredient.query.all()

    for ingredient in ingredients:
        ingredient_name = ingredient.ing_name
        ingredient_id = ingredient.ingredient_id
        # matching ingredient to product_id
        for key, value in prod_ing_dict.items():
            if ingredient_name in value:
                # creating product/ingredient instance
                product_ingredient = Product_Ingredient(product_id=key, 
                                                        ingredient_id=ingredient_id)
                db.session.add(product_ingredient)

    db.session.commit()


def load_flags(doc="seed_data/flags.txt"):
    """Loads flag data"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        name, description, citation, user_id = row.split("|")

        flag = Flag(name=name, 
                    description=description, 
                    citation=citation, 
                    user_id=user_id)

        db.session.add(flag)

    db.session.commit()


# def load_ingredient_flags(doc):
#     """Loads ingredient/flag data"""

#     for i, row in enumerate(open(doc)):
#         row = row.rstrip()
#         ingredient_id, flag_id = row.split("|")

#         ingredient_flag = Ingredient_Flag(ingredient_id=ingredient_id, 
#                                           flag_id=flag_id)

#         db.session.add(ingredient_flag)

#     db.session.commit()


# def load_categories(doc):
#     """Loads product category data"""

#     for i, row in enumerate(open(doc)):
#         row = row.rstrip()
#         product_id, broad, middle, specific = row.split("|")

#         category = Category(product_id=product_id, 
#                             broad=broad, 
#                             middle=middle, 
#                             specific=specific)

#         db.session.add(category)

#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()


    load_products("test_seed_data/test_valid_skin_urls.txt")
    load_ingredients()
    load_product_ingredients()
    load_flags("test_seed_data/test_flags.txt")










