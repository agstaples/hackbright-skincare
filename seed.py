"""Seeds skincare database from csv and txt files"""

from sqlalchemy import func
from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, Pregnancy_Flag, Sensitive_Flag
from server import app
import os
# from sephora_scrape import scrape_relevant_product_info

def load_products():
    """Loads product data from Sephora scrape"""

    for i in range(840):
        f = open(f"test_text/{i+1}", "r")
        text = f.readlines()
        url, pr_name, cat_1, cat_2, cat_3, brand, stars, price, ing = text[0].split("|")
        product = Product(sephora_url=url, 
                          pr_name=pr_name, 
                          brand=brand, 
                          stars=stars, 
                          price=price)

        db.session.add(product)

    db.session.commit()


def load_ingredients(doc):
    """Loads ingredient data"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        ing_name, synonyms = row.split("|")

        ingredient = Ingredient(ing_name=ing_name, 
                                synonyms=synonyms)

        db.session.add(ingredient)

    db.session.commit()


def load_product_ingredients(doc):
    """Loads product/ingredient data"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        product_id, ingredient_id = row.split("|")

        product_ingredient = Product_Ingredient(product_id=product_id, 
                                                ingredient_id=ingredient_id)

        db.session.add(product_ingredient)

    db.session.commit()


def load_users(doc):
    """Loads user data"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        fname, lname, email, password, m_f, concerns = row.split("|")

        user = User(fname=fname, 
                    lname=lname, 
                    email=email, 
                    password=password, 
                    m_f=m_f, 
                    concerns=concerns)

        db.session.add(user)

    db.session.commit()


def load_flags(doc):
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


def load_ingredient_flags(doc):
    """Loads ingredient/flag data"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        ingredient_id, flag_id = row.split("|")

        ingredient_flag = Ingredient_flag(ingredient_id=ingredient_id, 
                                          flag_id=flag_id)

        db.session.add(ingredient_flag)

    db.session.commit()


def load_categories(doc):
    """Loads product category data"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        product_id, broad, middle, specific = row.split("|")

        category = Category(product_id=product_id, 
                            broad=broad, 
                            middle=middle, 
                            specific=specific)

        db.session.add(category)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()


    load_products()







