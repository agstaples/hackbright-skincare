"""Models and database functions"""

from flask_sqlalchemy import SQLALchemy


db = SQLALchemy()


# table definitions:

class Product(db.Model):
    """Sephora product info and ingredients list"""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    pr_name = db.Column(db.String(75))
    brand = db.Column(db.String(75), 
                         nullable=True)
    sephora_url = db.Column(db.String(75),)
    stars = db.Column(db.String(75), 
                      nullable=True)
    price = db.Column(db.String(75), 
                      nullable=True)
    category_1 = db.Column(db.String(25))
    category_2 = db.Column(db.String(25), 
                           nullable=True)
    category_3 = db.Column(db.Column(db.String(25), 
                           nullable=True)
    ingredients = db.Column(db.String(1000),)


    def __repr__(self):
        """For easier id when printing"""

        return f"<Product product_id={product_id} pr_name={pr_name} brand={brand}>"


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


class Ingredient(db.Model):
    """Ingredient list with synonyms"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    ing_name = db.Column(db.String(75))
    synonyms = db.Column(db.String(500), 
                         nullable=True)
    euro_flag_id = db.Column(db.Integer, 
                             db.ForeignKey("euro_flags.euro_flag_id"), 
                             nullable=True)
    can_flag_id = db.Column(db.Integer, 
                            db.ForeignKey("can_flags.can_flag_id"), 
                            nullable=True)
    fda_flag_id = db.Column(db.Integer, 
                            db.ForeignKey("fda_flags.fda_flag_id"), 
                            nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Ingredient ingredient_id={ingredient_id} ing_name={pr_name}>"


class Pregnancy_Flag(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "pregnancy_flags"

    preg_flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    preg_notes = db.Column(db.String(500), 
                         nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Pregnancy Flag notes={preg_notes}>"


class Sensitive_Flag(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "sensitive_flags"

    sens_flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    sens_notes = db.Column(db.String(500), 
                         nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Sensitive Flag notes={sens_notes}>"


def connect_to_db(app):
    """Connect database to Flask app"""

    # Configuring for PostgreSQL db
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://skincare"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    """Allows you to work with db directly when you run in interactive mode"""

    from server import app
    connect_to_db(app)
    print("Connected to db")
















