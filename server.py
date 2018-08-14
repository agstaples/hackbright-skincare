"""Skincare Search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, products_schema, ingredients_schema, flags_schema, users_schema

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


@app.route("/register", methods=["POST"])
def process_registration():
    """Loads new user data to database"""

    fname = request.form["fname"]
    email = request.form["email"]
    password = request.form["password"]

    # checking if user already exists in database
    if User.query.filter_by(email=email).first():
        flash("That email address already exists in our files, please login.")
        return redirect("/login")
    # creating new user
    else:
        user = User(fname=fname, 
                    email=email, 
                    password=password)

    # commiting new user to database
    db.session.add(user)
    db.session.commit()

    flash("You successfully registered. Let's get searching.")
    return redirect("/search")


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

    auto_add_ing = user_flag_response[0]
    confirm_add_ing = user_flag_response[1]

    # if matches 99 or 100 matches, and no close matches create flag in database:
    if auto_add_ings != [] and confirm_add_ing == []:
        user_flag = Flag(name=user_flag_name, 
            ingredients_list=auto_add_ings, 
            user_id=user_id)

        # commiting new user flag to database
        db.session.add(user_flag)
        db.session.commit()

    # if close matches: add to session and send back to user:
    if confirm_add_ing != []:    
        session["user_flag_info"] = (user_flag_name, auto_add_ing)


    # return matches between 85 & 99 for confirmation otherwise return []
    return jsonify(auto_add_ing=auto_add_ing, 
                   confirm_add_ing=confirm_add_ing, 
                   user_flag_name=user_flag_name)


@app.route("/user_flag_fuzz_ing_add.json", methods=["POST"])
def add_user_fuzz_ings():
    """creates custom user flag in database"""

    add_fuzz_ings = request.form.get("chechedIngs")
    flag_name = session["user_flag_info"][0]
    session_flag_ings = session["user_flag_info"][1]
    # concatinating original match list and user approved fuzzy matches:
    flag_ings = session_flag_ings + add_fuzz_ings
    user_id = session["user_id"]


    user_flag = Flag(name=flag_name, 
                ingredients_list=flag_ings, 
                user_id=user_id)

    # commiting new user flag to database
    db.session.add(user_flag)
    db.session.commit()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


    