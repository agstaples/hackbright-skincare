"""Seeds skincare database from csv and txt files"""

from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from sqlalchemy import func
from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag
from server import app
import os
from fuzzywuzzy import process, fuzz
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
            print(url)
            header = {"User-Agent":"Firefox"}
            request = Request(url, headers=header)
            page = urlopen(request)
            # creating BeautifulSoup object for parsing
            soup = BeautifulSoup(page, "html.parser")
            # getting product name
            name_object = soup.find(attrs={"class": "css-1g2jq23"})
            if name_object:
                name = name_object.string
                print(name)
                # getting category information
                category = soup.find(attrs={"class": "css-j60h5s"}).string
                if category != "Skincare":
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
                    images = soup.select('div.css-t6rz1k > svg > image')
                    for image in images:
                        image_url = f"https://www.sephora.com{image.get('xlink:href')}"
                    # creating product instance
                    product = Product(sephora_url=url, 
                              pr_name=name, 
                              brand=brand, 
                              stars=float(stars), 
                              price=float(price),
                              category=category,  
                              image_url=image_url, 
                              ingredients_list=ingredients)
                    db.session.add(product)
                else:
                    print("***NO CATEGORY***")
            else:
                print("***ERROR***")
                print(url)

    print("****Donezo!****")
    db.session.commit()


def create_product_ingredient_dictionary():
    """creates dictionary of product ingredients to populate ingredient and product_ingredient tables"""

    prod_ing_dict = {}

    
    products = Product.query.all()
    for product in products:
        product_id = product.product_id
        # adding product_id keys to dictionary
        prod_ing_dict[product_id] = []
        # getting list of ingredients for each product
        ingredients_all = product.ingredients_list.split(",")
        for ingredient_single in ingredients_all:
            # cleaning up individual ingredientt and adding as values to dictionary
            ingredient_single = ingredient_single.strip(" ").rstrip(".\n").rstrip(".\r")
            prod_ing_dict[product_id].append(ingredient_single)

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
        ingredient = Ingredient(ing_name=ingredient)

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

    with open(doc) as flags_doc:
        flags = flags_doc.readlines()
        for flag in flags:
            name, description, ingredients = flag.split("|")
            flag = Flag(name=name, 
                        description=description,
                        ingredients_list=ingredients)
            db.session.add(flag)

    db.session.commit()


def create_flag_ingredient_dictionary():
    """creates dictionary of flag ingredients to populate flag_ingredient table"""

    fl_ing_dict = {}

    flags = Flag.query.all()
    for flag in flags:
        flag_id = flag.flag_id
        # adding flag_id keys to dictionary
        fl_ing_dict[flag_id] = []
        # getting list of ingredients for each flag
        ingredients_all = flag.ingredients_list.split(",")
        for ingredient_single in ingredients_all:
            # cleaning up individual ingredientt and adding as values to dictionary
            ingredient_single = ingredient_single.strip(" ").rstrip(".\n").rstrip(".\r")
            fl_ing_dict[flag_id].append(ingredient_single)

    return fl_ing_dict


def load_ingredient_flags():
    """Loads ingredient/flag data"""

    fl_ing_dict = create_flag_ingredient_dictionary()

    # getting full list of unique ingredients
    ingredients = Ingredient.query.all()

    for ingredient in ingredients:
        ingredient_name = ingredient.ing_name
        ingredient_id = ingredient.ingredient_id
        # matching ingredient to product_id
        for key, value in fl_ing_dict.items():
            if ingredient_name in value:
                # creating product/ingredient instance
                ingredient_flag = Ingredient_Flag(flag_id=key, 
                                                  ingredient_id=ingredient_id)
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


def fuzz_flag_ingredients(ingredients):
    """Takes in list of flagged ingredients, returns list of 95% matches"""


    ingredients_all = Ingredient.query.all()

    ingredient_choices = []
    match_dict = {}

    for ingredient in ingredients_all:
        ingredient_choices.append(ingredient.ing_name)

    for ingredient in ingredients:
        ingredient_matches = process.extract(ingredient, ingredient_choices, scorer=fuzz.partial_ratio, limit = 5)
        match_dict[ingredient] = ingredient_matches

    print(match_dict)


ingredients_list = ['lead', 'triclosan', 'oxybenzone', 'bht', 'butylated hydroxyanisole', 'bha', 'butylated hydroxytoluene', 'coal tar', 'paraben', 'phthalates', 'formaldehyde', 'eda', 'dithanolamine', 'triethanolamine', 'toluene', 'retinoids', 'retin a', 'salycylic acid', 'bpa', 'bithionol', 'chlorofluorocarbon propellants', 'chloroform', 'hexachlorophene', 'mercury', 'methylene chloride', 'vinyl chloride', 'zirconium', 'talc', 'propyl paraben', 'butyl paraben', 'isopropyl paraben', 'isobutyl paraben', 'methyl paraben', 'diethanolamine', 'oleamide DEA', 'lauramide DEA', 'cocamide DEA', 'Avobenzone', 'homosalate', 'octisalate', 'octocrylene', 'oxybenzone', 'oxtinoxate', 'menthyl anthranilate', 'oxtocrylene', 'Salicylic acid', '3-hydroxypropionic acid', 'trethocanic acid', 'tropic acid', 'aluminum chloride hexahydrate', 'aluminium chlorohydrate', 'acetyl mercaptan', 'mercaptoacetate', 'mercaptoacetic acid', 'thiovanic acid', 'Dihydroxyacetone', 'ammonia', 'methylbenzene', 'toluol', 'antisal 1a', 'formaldehyde', 'quaternium-15', 'dimethyl-dimethyl', 'DMDM', 'hydantoin', 'imidazolidinyl urea', 'diazolidinyl urea', 'sodium hydroxymethylglycinate', '2-bromo-2-nitropropane-1,3-diol', 'bromopol', 'BzBP', 'DBP', 'DEP', 'DMP', 'diethyl phthalate', 'dibutyl phthalate', 'benzylbutyl phthalate', 'hydroquinone', 'idrochinone', 'quinol/1-4 dihydroxy benzene/1-4 hydroxy benzene', 'retinoic acid', 'retinyl palmitate', 'retinaldehyde', 'adapalene', 'tretinoin', 'tazarotene', 'isotretinoin', 'Vitamin A', 'Toluene', 'DHA', 'Thioglycolic acid', 'Beta hydroxy acid']



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # once ingredients cleaned up, run this to update flags:
    # fuzz_flag_ingredients(ingredients_list)

    # load_products("seed_data/valid_skin_urls.txt")
    # load_ingredients()
    # load_product_ingredients()
    # load_flags("test_seed_data/test_flags.txt")
    # load_ingredient_flags()










