import os

list_ingredients = []

source = "test_text/"
with open(f"seed_data/ingredients_checked", "w") as file_checked, open(f"seed_data/ingredients_check", "w") as file_check:
    for root, dirs, filenames in os.walk(source):
        for file in filenames:
            print(file)
            f = open(f"{source}{file}", "r")
            text = f.readlines()
            url, pr_name, cat_1, cat_2, cat_3, brand, stars, price, ing = text[0].split("|")
            if ing[0:5] == "Water":
                file_checked.write(ing+"\n")
                print("water")
            else:
                file_check.write(ing+"\n")
                print("check")

#         ings = ing.split(",")
#         for ing in ings:
#             ing = ing.strip(" ").rstrip(".\n")
#             list_ingredients.append(ing)

# ingredients = list(set(list_ingredients))

# with open(f"seed_data/ingredients_data", "w") as file:
#     for ingredient in ingredients:
#         file.write(ingredient+"\n")
#         print("yay")




