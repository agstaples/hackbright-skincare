# tried to run this and it ran for 20 minutes and then just said KILLED

from bs4 import BeautifulSoup
# import urllib3
import requests
# from urllib3.exceptions import HTTPError
from urllib.request import Request, urlopen


def getting_urls_from_sitemap(doc="products-sitemap.xml", tag_name="loc"):
    """Takes in a filename and tag (both as strings), runs through BeautifulSoup and returns list of urls to parse"""

    with open(doc) as sitemap:
        sitemap_soup = BeautifulSoup(sitemap, "lxml")

    urls = sitemap_soup.find_all(tag_name)
    all_urls = []
    
    for url in urls:
        all_urls.append(url.string)

    # code to write urls to separate file if needed:
    # with open("sephora_all_urls.data", "w") as all_urls_data:
    #     for url in urls:
    #         url = url.string
    #         all_urls_data.write(url+"\n")

    return all_urls


def divide_url_list():
    """Divides full list of urls into smaller lists for processing to avoid runtime errors"""
    
    all_urls = getting_urls_from_sitemap()

    # returns full list broken into chunks of 100 urls or fewer
    return [all_urls[x:x+100] for x in range(0, len(all_urls), 100)]
    

def make_sephora_page_soup():
    """Makes soup objects out of Sephora urls"""

    split_urls = divide_url_list()
    print(len(split_urls))
    valid_skincare_urls = []
    counter = 103

    with open("valid_skin_urls.txt", "w+") as valid_skin_urls:
        for urls in split_urls[104:]:
            counter += 1
            print(counter)
            for url in urls:
                url = str(url)
                print(url)
                # providing headers for client, otherwise request fails
                # http = urllib3.PoolManager()
                header = {"User-Agent":"Firefox"}
                request = Request(url, headers=header)
                # try:
                page = urlopen(request)
                # except HTTPError:
                #     pass
                # else:
                soup = BeautifulSoup(page, "html.parser")
                product_name = soup.find(attrs={"class": "css-1g2jq23"})
                if product_name == None:
                    pass
                else:
                    categories_1_2 = soup.find_all(attrs={"class": "css-u2mtre"})
                    if categories_1_2 == []:
                        pass
                    else:
                        category_1 = categories_1_2[0].string
                        if category_1 == "Skincare":
                            valid_skin_urls.write(url+"\n")
                            print("success")
                            valid_skincare_urls.append(url)

    return len(valid_skincare_urls)

def scrape_relevant_product_info(doc="valid_skin_urls.txt"):
    """Reads valid skincare product urls from external file and scrapes for relevant data"""

    counter = 0

    with open(doc) as valid_skin_urls:
        urls = valid_skin_urls.readlines()
        for url in urls:
            counter += 1
            url = str(url.rstrip())
            # providing headers for client, otherwise request fails
            header = {"User-Agent":"Firefox"}
            request = Request(url, headers=header)
            page = urlopen(request)
            soup = BeautifulSoup(page, "html.parser")
            name = soup.find(attrs={"class": "css-1g2jq23"}).string
            categories_1_2 = soup.find_all(attrs={"class": "css-u2mtre"})
            if len(categories_1_2) == 0:
                category_1 = soup.find(attrs={"class": "css-j60h5s"}).string
            else:
                category_1 = categories_1_2[0].string
            if len(categories_1_2) > 1:
                category_2 = categories_1_2[1].string
            else:
                category_2 = ""
            category_3 = category_3 = soup.find(attrs={"class": "css-j60h5s"}).string
            # getting brand name
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
            product_box = soup.find_all(attrs={'class': 'css-1juot2r'})
            ingredients_all = product_box[-1].text
            ingredients_list = ingredients_all.split("\n")
            if len(ingredients_list[-1]) < 1:
                ingredients = ingredients_list[-2].rstrip(".")
            else:
                ingredients = ingredients_list[-1].rstrip(".")
            print(counter)
            file = open(f"test_text/{counter}", "w")
            file.write(url+"|"+name+"|"+category_1+"|"+category_2+"|"+category_3+"|"+brand+"|"+stars+"|"+price+"|"+ingredients)


scrape_relevant_product_info()  







