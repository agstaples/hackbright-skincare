# tried to run this and it ran for 20 minutes and then just said KILLED

from bs4 import BeautifulSoup
import urllib3
import requests
from urllib3.exceptions import HTTPError


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
    #         all_urls_data.write(url)

    return all_urls


def make_sephora_page_soup():
    """Makes soup objects out of Sephora urls"""

    urls = getting_urls_from_sitemap()
    valid_skincare_urls = []
    valid_nonskincare_urls = []
    faulty_urls = []

    for url in urls:
        url = str(url)
        # providing headers for client, otherwise request fails
        http = urllib3.PoolManager()
        header = {"User-Agent": "Human"}
        request = requests.get(url, headers=header)
        try:
            page = request.text
        except HTTPError:
            # only found one url that errored out this way and it was not relevant to project so skipping it
            faulty_urls.append(url)
            pass
        else:
            soup = BeautifulSoup(page, "html.parser")
            product_name = soup.find(attrs={"class": "css-1g2jq23"})
            if product_name == None:
                faulty_urls.append(url)
                pass
            else:
                categories_1_2 = soup.find_all(attrs={"class": "css-u2mtre"})
                if categories_1_2 == []:
                    faulty_urls.append(soup)
                else:
                    category_1 = categories_1_2[0].string
                    if category_1 != "Skincare":
                        valid_nonskincare_urls.append(url)
                        pass
                    else:
                        valid_skincare_urls.append(url)
                        print(url)

    return valid_skincare_urls

make_sephora_page_soup()

# code for getting category information from soups
# category_3 = soup.find(attrs={"class": "css-j60h5s"}).string
# category_1 = categories_1_2[0].string
# if category_1 != "Skincare":
#     pass
# else:
#     if len(categories_1_2) > 1:
#         category_2 = categories_1_2[1].string
#     else:
#         category_2 = "No information available"  



# def remove_inactive_pages():
#     """Removes inactive pages"""

#     sephora_soups_all = make_sephora_page_soup()

#     active_soups = []

#     for soup in sephora_soups_all:
#         product_name = soup.find(attrs={"class": "css-1g2jq23"})
#         if product_name == None:
#             print("pass")
#             pass
#         else:
#             active_soups.append(soup)
#             print(product_name)

#     return active_soups

# remove_inactive_pages()

def seperate_faulty_soups():
    """Seperates faulty soups for further inpection"""

    active_soups = remove_inactive_pages()

    faulty_soups = []
    valid_soups = []

    for soup in active_soups:
        category_info_check = soup.find_all(attrs={"class": "css-u2mtre"})
        categories_1_2 = soup.find_all(attrs={"class": "css-u2mtre"})
        if categories_1_2 == []:
            faulty_soups.append(soup)
        else:
            valid_soups.append(soup)

    print(len(valid_soups))
    print(len(faulty_soups))
    return valid_soups, faulty_soups


# all_urls = getting_urls_from_sitemap()




# # def parse_sephora_soups():
# #     """Parses non-faulty soup objects to extract information for Products Class"""

# #     product_info = {}
# #     # getting product name from page and excluding pages that are no longer active
# #     product_name = soup.find(attrs={"class": "css-1g2jq23"})

# #     product_info[url] = []
# #     # getting brand information from page and creating tuple for uniqueness
# #     brand = soup.find(attrs={"class": "css-cjz2sh"}).string
# #     # getting star rating as percentage
# #     stars_object = soup.find(attrs={"class": "css-dtomnp"})
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



