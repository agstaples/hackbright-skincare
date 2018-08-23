"""Seeds skincare database from csv and txt files"""

from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from sqlalchemy import func, update
from sqlalchemy import update
from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag
from server import app
import os
from fuzzywuzzy import process, fuzz
import time
import csv
# from sephora_scrape import scrape_relevant_product_info

def load_products(doc="seed_data/valid_skin_urls.txt"):
    """Loads product data from Sephora scrape"""

    counter = 0
    fail_counter = 0
    failed_urls = []

    # getting already vetted urls from file
    with open(doc) as valid_skin_urls:
        urls = valid_skin_urls.readlines()
        for url in urls:
            url = str(url.rstrip())
            # providing headers for client, otherwise request fails
            print(url)
            header = {"User-Agent":"Firefox"}
            request = Request(url, headers=header)
            page = urlopen(request)
            time.sleep(5)
            # creating BeautifulSoup object for parsing
            soup = BeautifulSoup(page, "html.parser")
            # getting product name
            name_object = soup.find(attrs={"class": "css-at8tjb"})
            if name_object:
                name = name_object.string
                # getting category information
                # category = soup.select('div.css-1k9l7o4 > h1')
                # category = soup.find(attrs={"class": "css-c02gs2"}).string
                categories = soup.find_all(attrs={'class': 'css-1euk4ns'})
                if len(categories) > 0:
                    category = categories[-1].text
                    if category != "Skincare":
                        print("in")
                        # getting product brand
                        brand = soup.find(attrs={"class": "css-1lujsz0"}).string
                       # getting price from sephora page
                        price_string = soup.find(attrs={"class": "css-n8yjg7"}).string
                        if price_string == None:
                            price = str(0)
                        else:
                            price = str(price_string.strip("$"))
                        # product box contains all product information inculding ingredients
                        product_box = soup.find_all(attrs={'class': 'css-1vwy1pm'})
                        ingredients_all = product_box[-1].text
                        ingredients_list = ingredients_all.split("\n")
                        if len(ingredients_list[-1]) < 1:
                            ingredients = ingredients_list[-2].rstrip(".")
                        else:
                            ingredients = ingredients_list[-1].rstrip(".")
                        images = soup.select('div.css-1lnrgf6 > svg > image')
                        for image in images:
                            image_url = f"https://www.sephora.com{image.get('xlink:href')}"
                        # creating product instance
                        product = Product(sephora_url=url, 
                                  pr_name=name, 
                                  brand=brand,  
                                  price=float(price),
                                  category=category,  
                                  image_url=image_url, 
                                  ingredients_list=ingredients)
                        db.session.add(product)
                        db.session.commit()
                        print(counter)
                        counter += 1
                    else:
                        fail_counter += 1
                        failed_urls.append(url)
                else:
                    fail_counter += 1
                    failed_urls.append(url)
            else:
                fail_counter += 1
                failed_urls.append(url)
    
    print(f"succeeded: {counter}")
    print(f"failed: {fail_counter}")
    print(failed_urls)
    print("****Donezo!****")
    return


def create_product_ingredient_dictionary():
    """creates dictionary of product ingredients to populate ingredient and product_ingredient tables"""

    prod_ing_dict = {}

    products = Product.query.all()
    for product in products:
        product_id = product.product_id
        # adding product_id keys to dictionary
        prod_ing_dict[product_id] = []
        # getting list of ingredients for each product
        ingredients_all = product.ingredients_list
        ingredients_all_split = ingredients_all.split(",")
        for ing in ingredients_all_split:
            ingredient_single = ing.strip("\"}{").strip()
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

    return "Success"


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

def export_to_csv():
    """exporting data to csv"""

    with open("ing_list.csv", "w") as f:
        out = csv.writer(f, delimiter="|")

        for product in Product.query.all():
            out.writerow([product.product_id, product.ingredients_list])

    return "Complete"

def import_from_csv():
    """importing clean ingredient data from csv"""

    with open("ing_list.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            split = row[0].split("|")
            product_id = split[0]
            ingredients = [split[1]] + row[1:]
            product = Product.query.filter_by(product_id=product_id).first()
            product.ingredients_list = ingredients
        db.session.commit()
        print("Done!")

def test_ingredients_before_repop():
    """testing cleaned ingredients before repopulating tables"""

    prod_ing_dict = {}

    products = Product.query.all()
    for product in products:
        product_id = product.product_id
        # adding product_id keys to dictionary
        prod_ing_dict[product_id] = []
        # getting list of ingredients for each product
        ingredients_all = product.ingredients_list
        ingredients_all_split = ingredients_all.split(",")
        for ing in ingredients_all_split:
            ingredient_single = ing.strip("\"}{").strip()
            prod_ing_dict[product_id].append(ingredient_single)

    return prod_ing_dict

def print_test_ings():
    """prints ing for select products"""

    id_list = [74, 104, 106, 194, 255, 346, 367, 433, 634, 548, 619, 643]
    for prod_id in id_list:
        product = Product.query.filter_by(product_id=prod_id).first()
        print(prod_id)
        print(product.ingredients_list)
    print("Done")

def update_test_ings():
    """updates select prod ingredients"""

    id_ing_tuples_list = [(74, "Water, Dimethicone, Sd Alcohol 40-B, Talc, Methyl Methacrylate Crosspolymer, Isododecane, Cetyl Ethylhexanoate, Diisopropyl Sebacate, Triethylhexanoin, Lauryl Peg-9 Polydimethylsiloxyethyl Dimethicone, Glycerin, Dextrin Palmitate, Sucrose Tetrastearate Triacetate, Polybutylene Glycol, Ppg-9, Copolymer, Trimethylsiloxysilicate, Xylitol, Silica, Sodium Chloride, Peg, Ppg-14, 7 Dimethyl Ether, Saxifraga Sarmentosa Extract, Sophora Angustifolia Root Extract, Disteardimonium Hectorite, Isostearic Acid, Calcium Stearate, Trisodium Edta, Vinyl Dimethicone, Methicone Silsesquioxane Crosspolymer, Alcohol, Bht, Butylene Glycol, Stearic Acid, Sodium Metabisulfite, Syzygium Jambos Leaf Extract, Tocopherol, Polysilicone-2, Methylparaben, Fragrance, Iron Oxides, Avobenzone 2.5%, Octinoxate 4.9%, Octocrylene 5%, and Oxybenzone 3%"),
    (104, "Prunus Amygdalus Dulcis (Sweet Almond) Oil, Cyclopentasiloxane, Passiflora incarnata (Passionfruit) oil, Argania Spinosa (Argan) Oil, Homosalate 10%, Octocrylene 9%, Octinoxate 7.5%, Ethylhexyl Salicylate 5%"), 
    (106, "Acacia Farnesiana (ORGANIC Acacia) Extract, AcrylatesCopolymer, Amaranthus Caudatus Seed Extract (ORGANIC), Camellia Sinensis LeafExtract (ORGANIC), Caprylhydroxamic Acid, Caprylyl Glycol, Carthamus Tinctorius(Safflower) Oleosomes, Cirtus Aurantium Dulcis (ORGANIC Orange) Fruit Water, Dicaprylyl Carbonate, Euterpe Oleracea (ORGANIC Acai) Fruit Oil, Flavor, FragariaVesca (ORGANIC Strawberry) Fruit Extract, Glycerin (ORGANIC), Helianthus Annuus(ORGANIC Sunflower) Seed Extract, 2-Hexanediol, Linum Usitatissimum (ORGANICLinseed) Seed Oil, Oenothera Biennis (ORGANIC Evening Primrose) Oil, PlanktonExtract, Salvia Hispanica (ORGANIC Chia) Seed Oil, Trisodium EthylenediamineDisuccinate, Water, Xanthan Gum, Avobenzone 3%, Octinoxate 6.2%"), 
    (194, "Avobenzone 3.0%, Homosalate 10.0%, Octisalate 4.5%, Alcohol Denat., Octyldodecyl Neopentanoate, Butyloctyl Salicylate, Polyester-8, Acrylates, Octylacrylamide Copolymer, Ethylhexyl Methoxycrylene, Dimethicone, Trimethylsiloxysilicate, Tocopheryl Acetate, Ethylcellulose, Avobenzone 3.0%, Homosalate 10.0%, Octisalate 4.5%"), 
    (255, "Cyclopentasiloxane, Water, Coconut Alkanes, Isododecane, Glycerin, Polyglyceryl-3 Polydimethylsiloxyethyl Dimethicone, PEG, PPG-18, 18 Dimethicone, Adipic Acid, Neopentyl Glycol Crosspolymer, Lauryl Dimethicone, Triethoxysilylethyl Polydimethylsiloxyethyl Hexyl Dimethicone, Aluminum Hydroxide, Stearic Acid, Butylene Glycol, Phenoxyethanol, Synthetic Fluorphlogopite, Titanium Dioxide, Hydrogenated Polyisobutene, Actinidia Chinensis (Kiwi) Fruit Water, Coco-Caprylate, Caprate, Caprylyl Glycol, Ethylhexylglycerin, Hexylene Glycol, Alcohol, Sophora Flavescens Root Extract, Sodium Hyaluronate, Glycyrrhiza Uralensis (Licorice) Root Extract, Hydrogenated Lecithin, CI 77491, CI 77492, Titanium Dioxide, Zinc Oxide, Octinoxate"), 
    (346, "Water, Cyclopentasiloxane, Alcohol Denat., Silica, Dicaprylyl Ether, Styrene, Acrylates Copolymer, PEG-30 Dipolyhydroxystearate, Dimethicone, Cyclohexasiloxane, Polymethylsilsesquioxane, Nylon-12, Dicaprylyl Carbonate, Phenoxyethanol, Lauryl PEG, PPG-18, 18 Methicone, Sodium Chloride, Caprylyl Glycol, PEG-8 Laurate, Poly C10-30 Alkyl Acrylate, Disteardimonium Hectorite, Tocopherol, Isostearyl Alcohol, P-Anisic Acid, Disodium EDTA, Dodecene, Poloxamer 407, Avobenzone 3%, Homosalate 10.72%, Octisalate 3.21%, Octocrylene 6%, Oxybenzone 3.86%"), 
    (367, "Water, Isododecane, Polyester-8, Glycerin, Cetyl PEG, PPG-10, 1 Dimethicone, Potassium Cetyl Phosphate, Phenoxyethanol, Cetearyl Alcohol, Diisopropyl Sebacate, Isodecyl Neopentanoate, Lauryl Lactate, Ammonium Acryloyldimethyltaurate, VP Copolymer, Diethylhexyl, Syringylidenemalonate, Acrylates Copolymer, Cetyl Alcohol, Behenyl Alcohol, Ethylhexylglycerin, Glyceryl Stearate, Chlorphenesin, Xanthan Gum, Caprylyl Glycol, Palmitic Acid, Stearic Acid, Behenic Acid, Cetyl Behenate, Isostearyl Isostearate, Lauryl Alcohol, Myristyl Alcohol, Aniba Rosaeodora (Rosewood) Wood Oil, Citrus Aurantium Dulcis (Orange) Peel Oil, Citrus Limon (Lemon) Peel Oil, Eucalyptus Globulus Leaf Oil, Ocimum Basilicum (Basil) Flower, Leaf Extract, Pelargonium Graveolens Flower Oil, Pogostemon Cablin Oil, Limonene, Allantoin, Disodium EDTA, Thermus Thermophillus Ferment, Lecithin, Pentylene Glycol, Panthenol, Sodium Hydroxide, BHT, Cassia Alata Leaf Extract, Maltodextrin, Geraniol, Citral, 2-Hexanediol, Beta-Glucan, Citric Acid, Sodium Benzoate, Tocopherol, Potassium Sorbate, Avobenzone 3%, Octisalate 5%, Octinoxate 7.5%, Homosalate 10%"), 
    (433, "Water, Methyl Trimethicone, Butylene Glycol, Butyloctyl Salicylate, Neopentyl Glycol Diheptanoate, Butyrospermum Parkii (Shea Butter), Peg-100 Stearate, Silica, Dipentaerythrityl Tri-Polyhydroxystearate, Lauryl Peg-9 Polydimethylsiloxyethyl Dimethicone, Dimethicone, Glyceryl Stearate, Laurdimonium Hydroxypropyl Hydrolyzed Soy Protein, Rosmarinus Officinalis (Rosemary) Extract, Perilla Ocymoides Leaf Extract, Plankton Extract, Caffeine, Potassium Cetyl Phosphate, Sucrose, Styrene, Acrylates Copolymer, C30-38 Olefin, Isopropyl Maleate, Ma Copolymer, Cetyl Alcohol, Vp, Eicosene Copolymer, Ethylhexylglycerin, Ammonium Acryloyldimethyltaurate, Vp Copolymer, Peg-8 Laurate, Sodium Rna, Lecithin, Propyl Gallate, Arginine Ferulate, Tocopheryl Acetate, Caprylyl Glycol, Ascorbyl Tocopheryl Maleate, Stearic Acid, Xanthan Gum, Hexylene Glycol, Nordihydroguaiaretic Acid, Disodium Edta, Phenoxyethanol, Mica, Sodium Dehydroacetate, Oxybenzone 5.00% , Octisalate 5.00% , Homosalate 5.00% , Avobenzone 3.00% , Octocrylene 2.70%"), 
    (634, "Octinoxate (7.4%), Zinc Oxide (9.6%)"), 
    (548, "Dipropylene Glycol, Sd Alcohol 40-B, Glycerin, Hydrogenated Polydecene, Xylitol, Isododecane, Dimethicone, Peg-5 Glyceryl Stearate, Isostearic Acid, Silica, Phenyl Trimethicone, Triethanolamine, Xanthan Gum, Tocopheryl Acetate, Peg, Ppg-17, 4 Dimethyl Ether, Piperidinepropionic Acid, Phytosteryl Macadamiate, 2-O-Ethyl Ascorbic Acid, Prunus Speciosa Leaf Extract, Angelica Acutiloba Root Extract, Isodonis Japonicus Leaf, Stalk Extract, Camellia Sinensis Leaf Extract, Zanthoxylum Piperitum Peel Extract, Ppg-17, Glyceryl Stearate Se, Behenyl Alcohol, Behenic Acid, Stearic Acid, Batyl Alcohol, Peg-30 Phytosterol, Butylene Glycol, Carbomer, Disodium Edta, Alcohol, Bht, Cellulose Gum, Sodium Metaphosphate, Talc, Dextrin Palmitate, Tocopherol, Ethylparaben, Methylparaben, Fragrance, Iron Oxides, Avobenzone 1.5%, Octinoxate 7.4%, Octocrylene 2%, Oxybenzone 1%"), 
    (619, "Octinoxate 4.9%, Octocrylene 3%, Zinc Oxide 12.5%"), 
    (643, "Water, Dimethicone, Alcohol, Polyglyceryl-3 Polydimethylsiloxyethyl Dimethicone, Aluminum Hydroxide, Stearic Acid, Nylon-12, Peg-12 Dimethicone, Sodium Chloride, Phenoxyethanol, Fragrance, Peg, Ppg-18, 18 Dimethicone, Glycerin, Ethylhexylglycerin, Tocopheryl Acetate, Disodium Edta, Sanicula Europaea Extract, Butylene Glycol, Sodium Hyaluronate, Hydroxypropyltrimonium Maltodextrin Crosspolymer, Thermus Thermophillus Ferment, Lapsana Communis Flower, Leaf, Stem Extract, Ribes Nigrum(Black Currant) Bud Extract, Potassium Sorbate, Citric Acid, Camellia Sinensis Leaf Extract, Cucumismelo (Melon) Fruit Extract, Sodium Lauryl Sulfate, Titanium Dioxide 10.9%, Homosalate 4%, Octocrylene 4%, Oxybenzone 1.5%")]
    
    for pair in id_ing_tuples_list:
        product_id = pair[0]
        ingredients = pair[1]
        product = Product.query.filter_by(product_id=product_id).first()
        product.ingredients_list = ingredients
    db.session.commit()
    print("Done!")

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
    # export_to_csv()
    # import_from_csv()
    # test_ingredients_before_repop()
    # print_test_ings()
    # update_test_ings()










