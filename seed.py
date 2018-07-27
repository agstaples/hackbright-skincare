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
                          category_1=cat_1, 
                          category_2=cat_2, 
                          category_3=cat_3, 
                          brand=brand, 
                          stars=stars, 
                          price=price, 
                          ingredients=ing)

        db.session.add(product)

    db.session.commit()


def load_pregnancy_flags(doc):
    """Loads product data from Sephora scrape"""

    for i, row in enumerate(open(doc)):
        row = row.rstrip()
        preg_flag_name, other_names, ewg_score = row.split("|")

        pregnancy_flag = Pregnancy_Flag(preg_flag_name=preg_flag_name, 
                                        other_names=other_names, 
                                        ewg_preg_score=ewg_score)

        db.session.add(pregnancy_flag)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()


    load_products()
    # preg_filename = "seed_data/preg_flag"
    # load_pregnancy_flags(preg_filename)







