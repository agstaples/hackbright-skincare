"""Skincare Search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, products_schema

from search import search_by_term


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """Renders homepage"""

    return render_template("homepage.html")


@app.route("/register")
def show_registration_form():
    """Registration form for new users"""

    return render_template("registration.html")


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


@app.route("/login")
def show_login_form():
    """Log in form for exisiting users"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Processes login form for existing users"""

    email = request.form["email"]
    password = request.form["password"]

    # checking if user already exists in database
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("That email address does not exist in our files, please try again or click Register for new users.")
        return redirect("/")

    # checking if password valid
    if user.password != password:
        flash(f"Welcome back {user.fname}! Please try your password again, that wasn't quite right.")
        return redirect("/login")

    # adding user to session
    session["user_id"] = user.user_id

    flash("You're logged in. Let's get searching.")
    return redirect("/search")


@app.route("/logout")
def logout():
    """Logs out user"""

    # deleting user from session when they log out
    del session["user_id"]
    flash("You're logged out. Bye for now.")
    return redirect("/")


@app.route("/search")
def show_product_search():
    """shows main search page"""

    return render_template("search.html")


@app.route("/user_flag")
def show_custom_flag_form():
    """Shows form for user to create custom flag"""

    # shows user form for creating custom flags

@app.route("/user_flag", methods=["POST"])
def create_custom_flag():
    """Creates custom user flag"""

    # creates custom user flag and saves to database

@app.route("/search_results.json", methods=["POST"])
def return_search_results():
    """Returns search results as json to render on /search page"""

    user_query = request.form.get("user_search")

    search_response = search_by_term(user_query)
    # returns: (products, brands, categories, (match_1, match_2, match_3, match_4), ingredients, ingredient_names)

    # flash error or render search results based on search results
    if search_response:
        serialized_response = products_schema.dump(search_response[0])
        brands = search_response[1]
        categories = search_response[2]
        rankings = search_response[3]
        ingredient_names = search_response[5]
        ranking = []
        for rank in rankings:
            ranking.append(rank)
        return_response = jsonify(products=serialized_response, 
                                   brands=brands, 
                                   categories=categories, 
                                   ingredient_names=ingredient_names, 
                                   rank=ranking)
        return return_response


    else:
        flash("It doesn't look like that was a valid search. Please try again.")
        return redirect("/search")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


    