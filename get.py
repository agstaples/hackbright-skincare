
preg_flag_list = []

for i in range(5):
    f = open(f"test_text/{i+1}", "r")
    text = f.readlines()
    url, pr_name, cat_1, cat_2, cat_3, brand, stars, price, ing = text[0].split("|")
    
    ings = ing.split()
    for ing in ings:
        ing = ing.rstrip(".\n")
        list_ingredients.append(ing)

ingredients = list(set(list_ingredients))

print(ingredients)