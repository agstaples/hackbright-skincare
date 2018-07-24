# tried to run this and it ran for 20 minutes and then just said KILLED

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import pickle


def getting_urls_from_sitemap(doc="products-sitemap.xml", tag_name="loc"):
    """Takes in a filename and tag (both as strings), runs through BeautifulSoup and returns list of urls to parse"""

    with open(doc) as sitemap:
        sitemap_soup = BeautifulSoup(sitemap, "lxml")

    urls = sitemap_soup.find_all(tag_name)
    all_urls = []
    
    for url in urls:
        all_urls.append(url.string)

    with open("sephora_all_urls.data") as all_urls_data:
        # store the data as binary data stream
        pickle.dump(all_urls, all_urls_data)

    return True


def make_sephora_page_soup():
    """Makes soup objects out of Sephora urls"""

    urls = getting_urls_from_sitemap()
    sephora_soups = []

    for url in urls:
        url = str(url)
        # providing headers for client, otherwise request fails
        header = {"User-Agent": "Human"}
        request = Request(url, headers=header)
        try:
            page = urlopen(request)
        except HTTPError:
            # only found one url that errored out this way and it was not relevant to project so skipping it
            pass
        else:
            soup = BeautifulSoup(page, "html.parser")
            sephora_soups.append(soup)

    return sephora_soups_all


def remove_inactive_pages():
    """Removes inactive pages"""

    sephora_soups_all = make_sephora_page_soup()

    active_soups = []

    for soup in sephora_soups_all:
        product_name = soup.find(attrs={"class": "css-1g2jq23"})
        if product_name == None:
            pass
        else:
            active_soups.append(soup)

    return active_soups


def seperate_faulty_soups():
    """Seperates faulty soups for further inpection"""

    active_soups = remove_inactive_pages()

    faulty_soups = []
    valid_soups = []

    for soup in active_soups:
        category_info_check = soup.find_all(attrs={"class": "css-u2mtre"})

        if categories_1_2 == []:
            faulty_soups.append(soup)
        else:
            valid_soups.append(soup)

    print(len(valid_soups))
    print(len(faulty_soups))
    return valid_soups, faulty_soups


all_urls = getting_urls_from_sitemap()




# def parse_sephora_soups():
#     """Parses non-faulty soup objects to extract information for Products Class"""

#     product_info = {}
#     # getting product name from page and excluding pages that are no longer active
#     product_name = soup.find(attrs={"class": "css-1g2jq23"})

#     product_info[url] = []
#     # getting brand information from page and creating tuple for uniqueness
#     brand = soup.find(attrs={"class": "css-cjz2sh"}).string
#     # getting star rating as percentage
#     stars_object = soup.find(attrs={"class": "css-dtomnp"})
#     stars = float(stars_object["style"].strip("%").split(":")[-1])
#     # getting price from sephora page
#     price_string = soup.find(attrs={"class": "css-18suhml"}).string
#     if price_string == None:
#         price = 0
#     else:
#         price = float(price_string.strip("$"))
#     # getting product categories from page
#     categories_1_2 = soup.find_all(attrs={"class": "css-u2mtre"})
#     if categories_1_2 == []:
#         category_1 = "No information available"
#         category_2 = "No information available"
#         category_3 = "No information available"
#     else:
#         category_3 = soup.find(attrs={"class": "css-j60h5s"}).string
#         category_1 = categories_1_2[0].string
#         if len(categories_1_2) > 1:
#             category_2 = categories_1_2[1].string
#         else:
#             category_2 = "No information available"
    
#     print(category_1, category_2)






        # category1 = soup.find()
        # # product_box = soup.find_all(attrs={'class': 'css-1juot2r'})
        # product_box = soup.find_all(attrs={'class': 'css-1juot2r'})
        # print(product_box)

        # ingredients = str(product_box[-1]).strip('.</div>').split("<br/><br/>")[-1]



