"""Models and database functions"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# table definitions:
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
    ingredients = db.Column(db.String(500000),
                           nullable=True)


    # def __repr__(self):
    #     """For easier id when printing"""

    #     return f"<Product product_id={product_id} pr_name={pr_name} brand={brand}>"


class Ingredient(db.Model):
    """Ingredient list with synonyms"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    ing_name = db.Column(db.String(75))
    synonym = db.Column(db.String(200), 
                         nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Ingredient ingredient_id={ingredient_id} ing_name={pr_name}>"


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

        return f"<Product_Ingredients prod_ing_id={prod_ing_id}>"


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

        return f"<User name={fname}>"



class Flag(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "flags"

    flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(400))
    citation = db.Column(db.String(400))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.user_id"), 
                        nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Flag name={name}>"


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

        return f"<Ingredient Flag ingredient flag={ing_flag_id}>"


class Category(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    product_id = db.Column(db.Integer, 
                        db.ForeignKey("products.product_id"))
    broad = db.Column(db.String(50))
    middle = db.Column(db.String(75), 
                       nullable=True)
    specific = db.Column(db.String(100), 
                       nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Category category={broad}/{middle}/{specific}>"


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


