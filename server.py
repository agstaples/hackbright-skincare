"""Skincare Search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, Category


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
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


@app.route("/search", methods=["POST"])
def process_product_search():
    """Processes search"""

    # getting search terms from form
    # if doing brand/ingredient search: set product_search to empty
    if request.form["submit_btn"] == "ing_brand_search":
        user_ingredient_search = request.form["user_ingredient_search"]
        session["ingredient_search"] = user_ingredient_search.lower()
        user_brand_search = request.form["user_brand_search"]
        session["brand_search"] = user_brand_search.lower()
        session["product_search"] = ""
    # if doing product search: set ingredient_search and brand_search to empty
    elif request.form["submit_btn"] == "product_search":
        user_product_search = request.form["user_product_search"]
        session["product_search"] = user_product_search.lower()
        session["ingredient_search"] = ""
        session["brand_search"] = ""

    return redirect("/search_results")

@app.route("/search_results")
def show_search_results():
    """show search results"""

    user_ingredient_search = session["ingredient_search"]
    user_brand_search = session["brand_search"]
    user_product_search = session["product_search"]

    # getting relevant product information from ingredient name
    if user_ingredient_search != "":
        ingredient = Ingredient.query.filter_by(ing_name_lower=user_ingredient_search).first()
        ingredient_products = ingredient.ing_products

    # getting relevant product information from brand name
    if user_brand_search != "":
        brand_products = Product.query.filter_by(brand_lower=user_brand_search).all()
    
    # getting relevant product information from product name
    if user_product_search != "":
        product = Product.query.filter_by(pr_name_lower=user_product_search).first()
        response = []
        response.append(product, product.get_flags_by_product())
        return render_template("search_results.html", 
                               response=response)

    # executing search for ingredient and no brand
    if user_ingredient_search != "" and user_brand_search == "":
        response = ingredient_products
        return render_template("search_results.html", 
                               response=response)
    # executing search for brand and no ingredient
    elif user_brand_search != "" and user_ingredient_search == "":
        response = brand_products
        return render_template("search_results.html", 
                               response=response)
    # executing search for ingredient and brand
    elif user_brand_search != "" and user_ingredient_search != "":
        brand_ingredient_match_products = []
        for product in ingredient_products:
            if product.brand == user_brand_search:
                brand_ingredient_match_products.append(product)
        if len(brand_ingredient_match_products) > 0:
            response = brand_ingredient_match_products
            return render_template("search_results.html", 
                                       response=response)
        else:
            flash("It doesn't look like there are any products by that brand that include that ingredient. Try searching just by brand or ingredient.")
            return redirect("/search")
    else:
        flash("It doesn't look like those were valid entries, please try again.")
        return redirect("/search")


@app.route("/user_flag")
def show_custom_flag_form():
    """Shows form for user to create custom flag"""

    # shows user form for creating custom flags

@app.route("/user_flag", methods=["POST"])
def create_custom_flag():
    """Creates custom user flag"""

    # creates custom user flag and saves to database


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")