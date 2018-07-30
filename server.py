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

    # simple search page that has different functional layouts:
        # search by ingredient
        # search by brand
        # search by product
        # search by category
        # search by some combination
        # results show as list with visual composition of results by flag


@app.route("/search", methods=["POST"])
def process_product_search():
    """Processes search"""

    user_search = request.form["user_search"]
    session["search"] = user_search

    return redirect("/search_results")


@app.route("/search_results")
def show_search_results():
    """show search results"""

    user_search = session["search"]
    search = db.session.query(Product).filter(Ingredient.ing_name=="PPG-20 Methyl Glucose Ether").all()
    print(search[0].pr_name)

    return render_template("search_results.html", 
                           search=search)


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