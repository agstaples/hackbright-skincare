"""Skincare Search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, products_schema, ingredients_schema, flags_schema, users_schema

from search import search_by_term


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
    print("deleted")

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
    user_flag_ings_input = request.form.get("user_flag_ings")
    user_flag_ings_list = user_flag_ings_input.split(",")
    user_flag_ings = []
    for user_flag_ing in user_flag_ings_list:
        user_flag_ing.strip()
        user_flag_ings.append(user_flag_ing)

    user_flag_response = return_close_ing_matches(user_flag_ings)
    # returns: (auto_add_ing, confirm_add_ing)

    # alert close matches under 99 and over 90 (100 and 99 included automatically)
    if user_flag_response:
        auto_add_ing_serialized = ingredients_schema.dump(search_response[0])
        print(auto_add_ing_serialized)
        confirm_add_ing_serialized = ingredients_schema.dump(search_response[1])

        return_response = jsonify(confirm_add_ing=confirm_add_ing_serialized, 
                                  auto_add_ing=auto_add_ing_serialized)
        return return_response


    return None


@app.route("/user_flag_add.json", methods=["POST"])
def add_user_flag():
    """creates custom user flag in database"""






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


    