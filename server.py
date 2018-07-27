"""Skincare Search"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Product, Product_Ingredient, Ingredient, Pregnancy_Flag, Sensitive_Flag


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


@app.route("/register", methods=["POST"])
def process_registration():
    """Processes registration form for new users"""


@app.route("/login")
def show_login_form():
    """Log in form for exisiting users"""


@app.route("/login")
def process_login():
    """Processes login form for existing users"""


@app.route("/logout")
def logout():
    """Logs out user"""


@app.route("/search")
def show_product_search():
    """shows main search page"""


@app.route("/search", methods=["POST"])
def process_product_search():
    """Processes search"""













if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")