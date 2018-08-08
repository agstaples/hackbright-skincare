"""Models and database functions"""

from flask_sqlalchemy import SQLAlchemy
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
    stars = db.Column(db.Integer, 
                      nullable=True)
    price = db.Column(db.Integer, 
                      nullable=True)
    category = db.Column(db.String(150), 
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

    def get_flags(self):
        """returns flags associated with product"""

        response_flags = []
        for ingredient in self.prod_ingredients:
            for flag in ingredient.ing_flags:
                response_flags.append(flag)
        response_flags = list(set(response_flags))
        return response_flags

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
    synonym_lower = db.Column(db.String(200), 
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



class Flag(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "flags"

    flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(400))
    ingredients_list = db.Column(db.String(500000))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id"), 
                        nullable=True)


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


###### SCHEMA ######

class ProductSchema(Schema):
    """Product table schema"""

    product_id = fields.Int(dump_only=True)
    pr_name = fields.Str()
    brand = fields.Str()
    sephora_url = fields.Str()
    stars = fields.Int()
    price = fields.Int()
    category = fields.Str()
    image_url = fields.Str()


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


