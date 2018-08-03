# manages validation of form entries
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


class Login_Form(FlaskForm):
    """manages validation for user login form"""

    email_username = StringField("Email_Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])


class Registration_Form(Form):
    """manages validation for user registration form"""


class User_Flag_Form


class Search_Form



