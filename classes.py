classes

Products:

product_name
brand
sephora_url
ingredient_list
stars
price
category 1
category 2
category 3

class Product:
    """product specific information from Sephora scrape"""

    def __init__(self, product_info_list):
        self.product_name = product_info_list[0]
        self.brand = product_info_list[1]
        self.sephora_url = product_info_list[2]
        self.ingredient_list = product_info_list[3]
        self.stars = product_info_list[4]
        self.price = product_info_list[5]
        self.category_1 = product_info_list[6]
        self.category_2 = product_info_list[7]
        self.category_3 = product_info_list[8]


