"""Skincare Search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, User, Flag, Ingredient_Flag, Category

from werkzeug.exceptions import BadRequestKeyError

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

    if User.query.filter_by(email=email).first():
        flash("That email address already exists in our files, please login.")
        return redirect("/login")
    else:
        user = User(fname=fname, 
                    email=email, 
                    password=password)

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

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("That email address does not exist in our files, please try again or click Register for new users.")
        return redirect("/")

    if user.password != password:
        flash(f"Welcome back {user.fname}! Please try your password again, that wasn't quite right.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You're logged in. Let's get searching.")
    return redirect("/search")


@app.route("/logout")
def logout():
    """Logs out user"""

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

    if request.form["submit_btn"] == "ing_brand_search":
        user_ingredient_search = request.form["user_ingredient_search"]
        session["ingredient_search"] = user_ingredient_search
        user_brand_search = request.form["user_brand_search"]
        session["brand_search"] = user_brand_search
        session["product_search"] = ""
    elif request.form["submit_btn"] == "product_search":
        user_product_search = request.form["user_product_search"]
        session["product_search"] = user_product_search
        session["ingredient_search"] = ""
        session["brand_search"] = ""

    return redirect("/search_results")

@app.route("/search_results")
def show_search_results():
    """show search results"""

    user_ingredient_search = session["ingredient_search"]
    user_brand_search = session["brand_search"]
    user_product_search = session["product_search"]

    if user_ingredient_search != "":
        ingredient = Ingredient.query.filter_by(ing_name=user_ingredient_search).first()
        products = Product_Ingredient.query.filter_by(ingredient_id=ingredient.ingredient_id).all()
        product_ids = []
        for product in products:
            product_ids.append(product.product_id)
        ingredient_products = Product.query.filter(Product.product_id.in_(product_ids))
    
    if user_brand_search != "":
        brand_products = Product.query.filter_by(brand=user_brand_search).all()
    
    if user_product_search != "":
        response = Product.query.filter_by(pr_name=user_product_search).all()
        return render_template("search_results.html", 
                               response=response)

    if user_ingredient_search != "" and user_brand_search == "":
        response = ingredient_products
        return render_template("search_results.html", 
                               response=response)
    elif user_brand_search != "" and user_ingredient_search == "":
        response = brand_products
        return render_template("search_results.html", 
                               response=response)
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
    """Shows for for user to create custom flag"""

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