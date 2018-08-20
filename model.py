"""Models and database functions"""

from flask_sqlalchemy import SQLAlchemy
from flask import session
from marshmallow import Schema, fields


db = SQLAlchemy()


###### MODELS ######

class Product(db.Model):
    """Sephora product info and ingredients list"""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    pr_name = db.Column(db.String(1000))
    brand = db.Column(db.String(1000), 
                      nullable=True)
    sephora_url = db.Column(db.String(1000))
    price = db.Column(db.Integer, 
                      nullable=True)
    category = db.Column(db.String(1500), 
                           nullable=True)
    image_url = db.Column(db.String(1000),
                          nullable=True)
    ingredients_list = db.Column(db.String(500000),
                                 nullable=True)

    prod_ingredients = db.relationship("Ingredient",
                                       secondary="join(Product_Ingredient, Ingredient, Product_Ingredient.ingredient_id == Ingredient.ingredient_id)", 
                                       primaryjoin="and_(Product.product_id == Product_Ingredient.product_id)", 
                                       secondaryjoin="Ingredient.ingredient_id == Product_Ingredient.ingredient_id", 
                                       backref=db.backref("products",
                                                     order_by=product_id))


    def __repr__(self):
        """For easier id when printing"""

        return f"<Product product_id={self.product_id} pr_name={self.pr_name} brand={self.brand}>"


class Ingredient(db.Model):
    """Ingredient list with synonyms"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, 
                              autoincrement=True, 
                              primary_key=True)
    ing_name = db.Column(db.String(3000))
    synonym = db.Column(db.String(200), 
                        nullable=True)

    ing_products = db.relationship("Product",
                               secondary="join(Product_Ingredient, Product, Product_Ingredient.product_id == Product.product_id)", 
                               primaryjoin="and_(Ingredient.ingredient_id == Product_Ingredient.ingredient_id)", 
                               secondaryjoin="Product.product_id == Product_Ingredient.product_id", 
                               backref=db.backref("ingredients",
                                                  order_by=ingredient_id))

    ing_flags = db.relationship("Flag",
                                  secondary="join(Ingredient_Flag, Flag, Ingredient_Flag.flag_id == Flag.flag_id)", 
                                  primaryjoin="and_(Ingredient.ingredient_id == Ingredient_Flag.ingredient_id)", 
                                  secondaryjoin="Flag.flag_id == Ingredient_Flag.flag_id", 
                                  backref=db.backref("ingredients",
                                                     order_by=ingredient_id))

    def __repr__(self):
        """For easier id when printing"""

        return f"<Ingredient ingredient_id={self.ingredient_id} ing_name={self.ing_name}>"


class Product_Ingredient(db.Model):
    """Ingredient list with synonyms"""

    __tablename__ = "product_ingredients"

    prod_ing_id = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    product_id = db.Column(db.Integer, 
                           db.ForeignKey("products.product_id"), 
                           nullable=True)
    ingredient_id = db.Column(db.Integer, 
                              db.ForeignKey("ingredients.ingredient_id"), 
                              nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Product_Ingredients prod_ing_id={self.prod_ing_id}>"


class User(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    fname = db.Column(db.String(100))
    email = db.Column(db.String(75))
    password = db.Column(db.String(100))

    def __repr__(self):
        """For easier id when printing"""

        return f"<User name={self.fname}>"


class User_Flag(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "user_flags"

    user_flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    enabled = db.Column(db.Boolean, 
                        unique=False, 
                        default=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id"))
    flag_id = db.Column(db.Integer, 
                        db.ForeignKey("flags.flag_id"))

    flag_users = db.relationship("User", backref="users")
    users_flags = db.relationship("Flag", backref="flags")

    def __repr__(self):
        """For easier id when printing"""

        return f"<User Flag user flag={self.user_flag_id}>"



class Flag(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "flags"

    flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(400))
    ingredients_list = db.Column(db.String(500000))

    fl_ingredients = db.relationship("Ingredient",
                                  secondary="join(Ingredient_Flag, Ingredient, Ingredient_Flag.ingredient_id == Ingredient.ingredient_id)", 
                                  primaryjoin="and_(Flag.flag_id == Ingredient_Flag.flag_id)", 
                                  secondaryjoin="Ingredient.ingredient_id == Ingredient_Flag.ingredient_id", 
                                  backref=db.backref("flags",
                                                     order_by=flag_id))

    def __repr__(self):
        """For easier id when printing"""

        return f"<Flag flag_id={self.flag_id} name={self.name}>"


class Ingredient_Flag(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "ingredient_flags"

    ing_flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    ingredient_id = db.Column(db.Integer, 
                        db.ForeignKey("ingredients.ingredient_id"))
    flag_id = db.Column(db.Integer, 
                        db.ForeignKey("flags.flag_id"))


    def __repr__(self):
        """For easier id when printing"""

        return f"<Ingredient Flag ingredient flag={self.ing_flag_id}>"


###### SCHEMAS ######

class UserSchema(Schema):
    """Flag table schema"""

    user_id = fields.Int(dump_only=True)
    fname = fields.Str()
    email = fields.Str()
    password = fields.Str()

users_schema = UserSchema()


class FlagSchema(Schema):
    """Flag table schema"""

    flag_id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    ingredients_list = fields.Str()

flags_schema = FlagSchema(many=True)



class IngredientSchema(Schema):
    """Ingredient table schema"""

    ingredient_id = fields.Int(dump_only=True)
    ing_name = fields.Str()
    synonym = fields.Str()
    ing_flags = fields.Nested(FlagSchema, many=True)

ingredients_schema = IngredientSchema(many=True)



class ProductSchema(Schema):
    """Product table schema"""

    product_id = fields.Int(dump_only=True)
    pr_name = fields.Str()
    brand = fields.Str()
    sephora_url = fields.Str()
    price = fields.Int()
    category = fields.Str()
    image_url = fields.Str()
    prod_ingredients = fields.Nested(IngredientSchema, many=True)
    enabled_flags = fields.Method("get_enabled_flags")
    enabled_flag_ings = fields.Method("get_enabled_flag_ings")

    # method for returning flags:
    def get_enabled_flags(self, obj):
        """returns flags associated with product"""

        user_id = session["user_id"]
        response_flags = []
        for ingredient in obj.prod_ingredients:
            for flag in ingredient.ing_flags:
                user_flag = User_Flag.query.filter((User_Flag.flag_id==flag.flag_id) & (User_Flag.user_id==user_id)).first()
                if user_flag != None:
                    if user_flag.enabled == True:
                        response_flags.append(user_flag.users_flags.name)
        response_flags = list(set(response_flags))
        return response_flags

    # method for returning user flags and associated ings:
    def get_enabled_flag_ings(self, obj):
        """returns flags associated with product and specific user and flagged ings"""

        user_id = session["user_id"]
        response_flags_ings = {}
        for ingredient in obj.prod_ingredients:
            for flag in ingredient.ing_flags:
                user_flag = User_Flag.query.filter((User_Flag.flag_id==flag.flag_id) & (User_Flag.user_id==user_id)).first()
                if user_flag != None:
                    if user_flag.enabled == True:
                        if user_flag.users_flags.name in response_flags_ings:
                            response_flags_ings[user_flag.users_flags.name] += f", {ingredient.ing_name}"
                        else:
                            response_flags_ings[user_flag.users_flags.name] = f"{ingredient.ing_name}"
        return response_flags_ings


products_schema = ProductSchema(many=True)



###### DB ######

def connect_to_db(app):
    """Connect database to Flask app"""

    # Configuring for PostgreSQL db
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///skincare"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
    """Allows you to work with db directly when you run in interactive mode"""

    from server import app
    connect_to_db(app)
    print("Connected to db")


