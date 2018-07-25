"""Seeds skincare database from csv and txt files"""

from sqlalchemy import func
from model import Product, Product_Ingredient, Ingredient, Canadian_Flag, European_Flag, FDA_Flag
from server import app
from sephora_scrape_more_functions import scrape_relevant_product_info

def load_products(doc="products.csv"):
    """Loads product data from Sephora scrape"""

    product_details = scrape_relevant_product_info()

    for key, value in product_details.items():
        product_id, pr_name, brand, sephora_url, stars, price, cat_1, cat_2, cat_3, ing = value.split()
        product = Product(product_id=product_id, 
                          pr_name=pr_name, 
                          brand=brand, 
                          sephora_url=sephora_url, 
                          stars=stars, 
                          price=price, 
                          category_1=cat_1, 
                          category_2=cat_2, 
                          category_3=cat_3, 
                          ingredients=ing)

        db.session.add(product)

    db.session.commit()


def load_product_ingredients(doc="product_ingredients.csv"):
    """Loads product data from Sephora scrape"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        product_id, pr_name, brand, sephora_url, stars, price = row.split(",")

        product = Product(product_id=product_id, 
                          pr_name=pr_name, 
                          brand=brand, 
                          sephora_url=sephora_url, 
                          stars=stars, 
                          price=price)

        db.session.add(product)

    db.session.commit()


def load_product_ingredients(doc="product_ingredients.csv"):
    """Loads product data from Sephora scrape"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        product_id, pr_name, brand, sephora_url, stars, price = row.split(",")

        product = Product(product_id=product_id, 
                          pr_name=pr_name, 
                          brand=brand, 
                          sephora_url=sephora_url, 
                          stars=stars, 
                          price=price)

        db.session.add(product)

    db.session.commit()









