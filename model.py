"""Models and database functions"""

from flask_sqlalchemy import SQLALchemy


db = SQLALchemy()


# table definitions:

class Products(db.Model):
    """Sephora product info and ingredients list"""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    pr_name = db.Column(db.String(75))
    brand = db.Column(db.String(75), 
                         nullable=True)
    sephora_url = db.Column(db.String(75),)
    ingredient_list = db.Column(db.String(500))
    stars = db.Column(db.String(75), 
                      nullable=True)
    price = db.Column(db.String(75), 
                      nullable=True)
    category_1 = db.Column(db.String(25))
    category_2 = db.Column(db.String(25), 
                           nullable=True)
    category_3 = db.Column(db.Column(db.String(25), 
                           nullable=True)


    def __repr__(self):
        """For easier id when printing"""

        return f"<Product product_id={product_id} pr_name={pr_name} brand={brand}>"


class Ingredients(db.Model):
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


class Canadian_Flags(db.Model):
    """Canadian ingredient flags and notes"""

    __tablename__ = "canadian_flags"

    can_flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    ingredient_id = db.Column(db.Integer, 
                              db.ForeignKey("ingredients.ingredient_id"), 
                              nullable=True)
    can_notes = db.Column(db.String(75))
    can_severity = db.Column(db.String(500), 
                         nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<Canadian Flag severity={can_severity}>"


class European_Flags(db.Model):
    """European ingredient flags and notes"""

    __tablename__ = "european_flags"

    euro_flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    ingredient_id = db.Column(db.Integer, 
                              db.ForeignKey("ingredients.ingredient_id"), 
                              nullable=True)
    euro_notes = db.Column(db.String(75))
    euro_severity = db.Column(db.String(500), 
                         nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<European Flag severity={euro_severity}>"


class FDA_Flags(db.Model):
    """FDA ingredient flags and notes"""

    __tablename__ = "fda_flags"

    fda_flag_id = db.Column(db.Integer, 
                           autoincrement=True, 
                           primary_key=True)
    ingredient_id = db.Column(db.Integer, 
                              db.ForeignKey("ingredients.ingredient_id"), 
                              nullable=True)
    fda_notes = db.Column(db.String(75))
    fda_severity = db.Column(db.String(500), 
                         nullable=True)

    def __repr__(self):
        """For easier id when printing"""

        return f"<FDA Flag severity={fda_severity}>"
















