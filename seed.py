"""Seeds skincare database from csv and txt files"""

from sqlalchemy import func
from model import Product, Product_Ingredient, Ingredient, Pregnancy_Flag, Sensitive_Flag
from server import app
from sephora_scrape_more_functions import scrape_relevant_product_info

def load_products(doc="products.csv"):
    """Loads product data from Sephora scrape"""

    product_details = scrape_relevant_product_info()

    for key, value in product_details.items():
        pr_name, brand, sephora_url, stars, price, cat_1, cat_2, cat_3, ing = value.split()
        product = Product(pr_name=pr_name, 
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


def load_pregnancy_flags(doc="pregnancy_flags.csv"):
    """Loads product data from Sephora scrape"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        preg_flag_name, synonyms, preg_notes = row.split(",")

        pregnancy_flag = Pregnancy_Flag(preg_flag_name=preg_flag_name, 
                                        synonyms=synonyms, 
                                        preg_notes=preg_notes)

        db.session.add(pregnancy_flag)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    preg_flag_filename = "seed_data/u.item"
    load_pregnancy_flags(user_filename)





