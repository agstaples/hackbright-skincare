"""Skincare Search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, User_Flag, Ingredient_Flag, products_schema, ingredients_schema, flags_schema, users_schema

from search import search_by_term, return_close_ing_matches


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route("/user_validation.json")
def check_for_user():
    """CHecks if user is logged in"""

    user_id = session.get("user_id")

    
    if user_id:
        user = User.query.get(user_id)
        user_serialized = users_schema.dump(user)
        return jsonify(user=user_serialized)

    return "No"


@app.route("/user_register.json", methods=["POST"])
def process_registration():
    """Loads new user data to database"""

    print("in route")

    fname = request.form.get("fname")
    email = request.form.get("email")
    password_1 = request.form.get("password_1")
    password_2 = request.form.get("password_2")

    # checking if user already exists in database
    if User.query.filter_by(email=email).first():
        return redirect("Not unique")
    # creating new user
    elif password_1 != password_2:
        return "No"

    else:
        user = User(fname=fname, 
                    email=email, 
                    password=password_1)

        db.session.add(user)
        db.session.flush()

        user_id = user.user_id
        db.session.commit()
        session["user_id"] = user_id
        user_flag_1 = User_Flag(user_id=user_id, 
                                flag_id=1)
        db.session.add(user_flag_1)
        user_flag_2 = User_Flag(user_id=user_id, 
                                flag_id=2)
        db.session.add(user_flag_2)
        db.session.commit()
        return "Yes"

    return "No"


@app.route("/user_login.json", methods=["POST"])
def process_login():
    """Processes login form for existing users"""

    user_query = request.form.get("user_search")

    email = request.form.get("email")
    password = request.form.get("password")

    # checking if user already exists in database
    user = User.query.filter_by(email=email).first()

    if not user:
        return "No"

    # checking if password valid
    if user.password != password:
        return "No"

    # adding user to session
    session["user_id"] = user.user_id

    return user.fname


@app.route("/logout.json")
def logout():
    """Logs out user"""

    # deleting user from session when they log out
    del session["user_id"]

    return "You have successfully signed out"


@app.route("/search")
def show_product_search():
    """shows main search page"""

    return render_template("search.html")


@app.route("/search_results.json", methods=["POST"])
def return_search_results():
    """Returns search results as json to render on /search page"""

    user_query = request.form.get("user_search")

    search_response = search_by_term(user_query)
    # returns: (products, brands, categories, (match_1, match_2, match_3, match_4), ingredients)

    # flash error or render search results based on search results
    if search_response:
        prods_serialized_response = products_schema.dump(search_response[0])
        ings_serialized_response = ingredients_schema.dump(search_response[4])
        brands = search_response[1]
        categories = search_response[2]
        rankings = search_response[3]
        ranking = []
        for rank in rankings:
            ranking.append(rank)
        return_response = jsonify(products=prods_serialized_response, 
                                   brands=brands, 
                                   categories=categories, 
                                   ingredients=ings_serialized_response, 
                                   rank=ranking)
        return return_response


    return None


@app.route("/user_flag_ing_check.json", methods=["POST"])
def return_flag_close_ings():
    """Returns search results as json to render on /search page"""

    user_flag_name = request.form.get("user_flag_name")
    session["user_flag_info"] = ("", [])
    user_id = session["user_id"]
    user_flag_ings_input = str(request.form.get("user_flag_ings"))
    user_flag_ings_list = user_flag_ings_input.split(",")
    user_flag_ings = []
    for user_flag_ing in user_flag_ings_list:
        user_flag_ing.strip()
        user_flag_ings.append(user_flag_ing)

    user_flag_response = return_close_ing_matches(user_flag_ings)
    # returns: (auto_add_ing, confirm_add_ing)

    auto_add_ings = user_flag_response[0]
    confirm_add_ings = user_flag_response[1]

    session["user_flag_info"] = (user_flag_name, auto_add_ings)
    if len(confirm_add_ings) < 1 and len(auto_add_ings) > 0:
        flag = Flag(name=user_flag_name, 
                    ingredients_list=auto_add_ings)
        db.session.add(flag)
        db.session.flush()

        flag_id = flag.flag_id
        user_flag = User_Flag(flag_id=flag_id, 
                              user_id=user_id)
        db.session.add(user_flag)
        db.session.commit()

        load_ingredient_flags()
    print("wtf")

    # return matches between 85 & 99 for confirmation otherwise return []
    return jsonify(auto_add_ing=auto_add_ings, 
                   confirm_add_ing=confirm_add_ings, 
                   user_flag_name=user_flag_name)


@app.route("/user_flag_fuzz_ing_add.json", methods=["POST"])
def add_user_fuzz_ings():
    """creates custom user flag in database"""

    # add_fuzz_ings = request.get("chechedIngs")
    # add_fuzz_ings = request.POST["chechedIngs"]
    add_fuzz_ings = request.form.getlist("ings[]")
    flag_name = session["user_flag_info"][0]
    auto_add_ings = session["user_flag_info"][1]
    flag_ings = []
    for flag in add_fuzz_ings:
        flag_ings.append(flag)
    for flag in auto_add_ings:
        flag_ings.append(flag)
    user_id = session["user_id"]

    flag = Flag(name=flag_name, 
                ingredients_list=flag_ings)
    db.session.add(flag)
    db.session.flush()

    flag_id = flag.flag_id
    user_flag = User_Flag(flag_id=flag_id, 
                          user_id=user_id)
    db.session.add(user_flag)
    db.session.commit()

    load_ingredient_flags()

    return "SUCCESS!!!"


def create_flag_ingredient_dictionary():
    """creates dictionary of flag ingredients to populate flag_ingredient table"""

    user_id = session["user_id"]

    fl_ing_dict = {}

    user_flags = User_Flag.query.filter(User_Flag.user_id == user_id).all()

    for user_flag in user_flags:
        flag_id = user_flag.flag_id
        # adding flag_id keys to dictionary
        fl_ing_dict[flag_id] = []
        flag = Flag.query.filter(Flag.flag_id == flag_id).first()
        # getting list of ingredients for each flag
        ingredients_all = flag.ingredients_list.strip("'\"{'}").split(",")
        for ingredient_single in ingredients_all:
            ingredient_single = str(ingredient_single.strip("'\"{'}"))
            # cleaning up individual ingredientt and adding as values to dictionary
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


@app.route("/flag_info.json", methods=["POST"])
def disable_enable_flag():
    """Decativates and/or activates exisiting flags"""

    user_id = session["user_id"]
    # not correct, need to pull from user_Flag table:
    user_flags = User_Flag.query.filter(User_Flag.user_id == user_id).all()
    enabled_flags = []
    disabled_flags = []
    for flag in user_flags:
        response_flag = Flag.query.filter(Flag.flag_id == flag.flag_id).first()
        if flag.enabled:
            enabled_flags.append(response_flag.name)
        else:
            disabled_flags.append(response_flag.name)

    return jsonify(enabled_flags=enabled_flags, 
                   disabled_flags=disabled_flags)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


    