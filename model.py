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
    pr_name_lower = db.Column(db.String(1000))
    brand = db.Column(db.String(1000), 
                      nullable=True)
    brand_lower = db.Column(db.String(1000), 
                            nullable=True)
    sephora_url = db.Column(db.String(1000))
    stars = db.Column(db.Integer, 
                      nullable=True)
    price = db.Column(db.Integer, 
                      nullable=True)
    ingredients_list = db.Column(db.String(500000),
                                 nullable=True)

    prod_ingredients = db.relationship("Ingredient",
                                  secondary="join(Product_Ingredient, Ingredient, Product_Ingredient.ingredient_id == Ingredient.ingredient_id)", 
                                  primaryjoin="and_(Product.product_id == Product_Ingredient.product_id)", 
                                  secondaryjoin="Ingredient.ingredient_id == Product_Ingredient.ingredient_id", 
                                  backref=db.backref("products",
                                                     order_by=product_id))

    
    def get_ingredients_by_product(self):
        """returns ingredient associated with product"""

    def get_flags_by_product(self):
        """returns flags associated with product"""

        # response_flags = []
        # for ingredient in self.ingredients:
        #     return ingredient.flags
        #     # you need to set up flag to ingredient table relationships,
        #     # then you can finish this code here, that will be used on 
        #     # line 153 of server.py
        
        # return response_products

    def get_categories_by_product(self):
        """returns categories associated with product"""

    def __repr__(self):
        """For easier id when printing"""

        return f"<Product product_id={self.product_id} pr_name={self.pr_name} brand={self.brand}>"


class Ingredient(db.Model):
    """Ingredient list with synonyms"""

    __tablename__ = "ingredients"

    ingredient_id = db.Column(db.Integer, 
                              autoincrement=True, 
                              primary_key=True)
    ing_name = db.Column(db.String(75))
    ing_name_lower = db.Column(db.String(75))
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


    def get_products_by_ingredient(self):
        """returns products associated with ingredient"""

        response_products = []
        for product_ingredient in self.products:
            response_products.append(product_ingredient.products)
        
        return response_products

    def get_flags_by_ingredient(self):
        """returns flags associated with ingredient"""

    def get_categories_by_ingredient(self):
        """returns categories associated with ingredient"""

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

    def get_flags_by_user(self):
      """returns flags associated with user. all global flags and any custom user flags"""

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


    def get_products_by_flag(self):
        """returns products associated with flag"""

    def get_ingredients_by_flag(self):
        """returns ingredients associated with flag"""

    def get_categories_by_flag(self):
        """returns categories associated with flag"""

    def __repr__(self):
        """For easier id when printing"""

        return f"<Flag name={self.name}>"


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

    def get_products_by_category(self):
        """returns products associated with category"""

    def get_ingredients_by_category(self):
        """returns ingredients associated with category"""

    def get_flags_by_category(self):
        """returns flags associated with category"""

    def __repr__(self):
        """For easier id when printing"""

        return f"<Category category={self.broad}/{self.middle}/{self.specific}>"


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


