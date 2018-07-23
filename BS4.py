from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


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
        page = urlopen(request)
        soup = BeautifulSoup(page, "html.parser")
        
        # getting product name from page and excluding pages that are no longer active
        product_name = soup.find(attrs={"class": "css-1g2jq23"})
        if product_name == None:
            pass
        else:
            product_info[url] = []
            # getting brand information from page and creating tuple for uniqueness
            brand = soup.find(attrs={"class": "css-cjz2sh"}).string
            # getting star rating as percentage
            stars_object = soup.find(attrs={"class": "css-dtomnp"})
            stars = float(stars_object["style"].strip("%").split(":")[-1])
            print(stars)
            # getting price from sephora page
            price_string = soup.find(attrs={"class": "css-18suhml"}).string
            price = float(price_string.strip("$"))






        
        # # getting product category information from page. category_box_1 is most general
        # category_box = soup.find_all(attrs={"class": "css-u2mtre"})
        # for category in category_box:
        #     category.string)
        # category_box_2 = 
        # category_box_3 = 
        
parse_sephora_product_pages()



        # category1 = soup.find()
        # # product_box = soup.find_all(attrs={'class': 'css-1juot2r'})
        # product_box = soup.find_all(attrs={'class': 'css-1juot2r'})
        # print(product_box)

        # ingredients = str(product_box[-1]).strip('.</div>').split("<br/><br/>")[-1]



