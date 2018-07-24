from bs4 import BeautifulSoup
import urllib3
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def getting_urls_from_sitemap(doc="products-sitemap.xml", tag_name="loc"):
    """Takes in a filename and tag (both as strings), runs through BeautifulSoup and returns list of urls to parse"""

    with open(doc) as sitemap:
        sitemap_soup = BeautifulSoup(sitemap, "lxml")

    urls = sitemap_soup.find_all(tag_name)
    parsed_urls = []
    
    for url in urls:
        parsed_urls.append(url.string)

    return parsed_urls


def parse_sephora_product_pages():
    """Takes in list of Sephora product page URLs and parses relevant information"""

    urls = getting_urls_from_sitemap()
    product_info = {}

    for url in urls:
        url = str(url)
        # providing headers for client, otherwise request fails
        header = {"User-Agent": "Human"}
        request = Request(url, headers=header)
        try:
            page = urlopen(request)
        except HTTPError:
            pass
        else:
            soup = BeautifulSoup(page, "html.parser")
        
            # getting product name from page and excluding pages that are no longer active
            product_name = soup.find(attrs={"class": "css-1g2jq23"})

            #save these links.
            #create a new function to open said links.


            if product_name == None:
                pass
            else:
                product_info[url] = []
                # getting product categories from page
                categories_1_2 = soup.find_all(attrs={"class": "css-u2mtre"})
                if categories_1_2 == []:
                    category_1 = "No information available"
                    category_2 = "No information available"
                    category_3 = "No information available"
                else:
                    category_3 = soup.find(attrs={"class": "css-j60h5s"}).string
                    category_1 = categories_1_2[0].string
                    if category_1 != "Skincare":
                        pass
                    else:
                        if len(categories_1_2) > 1:
                            category_2 = categories_1_2[1].string
                        else:
                            category_2 = "No information available"                
                    # getting brand information from page and creating tuple for uniqueness
                    brand = soup.find(attrs={"class": "css-cjz2sh"}).string
                    # getting star rating as percentage
                    stars_object = soup.find(attrs={"class": "css-dtomnp"})
                    if stars_object == None:
                        stars = 0
                    else:
                        stars = float(stars_object["style"].strip("%").split(":")[-1])
                    # getting price from sephora page
                    price_string = soup.find(attrs={"class": "css-18suhml"}).string
                    if price_string == None:
                        price = 0
                    else:
                        price = float(price_string.strip("$"))
                    # getting product ingredients
                    product_box = soup.find_all(attrs={"class": "css-1juot2r"})
                    if len(product_box) < 3:
                        ingredients = "No information available"
                    else:
                        ingredients = str(product_box[2]).strip('.</div>').split(">")[-1]


parse_sephora_product_pages()



