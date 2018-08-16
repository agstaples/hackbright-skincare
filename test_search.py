

from search import search_by_term, return_close_ing_matches
import unittest




class SkincareSearchUnitTestCase(unittest.TestCase):
    """Class of tests to test functions in search.py"""


    def test_search_by_term_1(self):
        """tests search_by_term function"""

        assert search_by_term("water") == ([<Product product_id=3 pr_name=Sake Bright White Mask brand=boscia>, 
                                           <Product product_id=2 pr_name=Radiant Moisture Souffle  brand=TOM FORD>, 
                                           <Product product_id=4 pr_name=Sports BB Broad Spectrum SPF 50+ WetForce brand=Shiseido>, 
                                           <Product product_id=5 pr_name=Oxygen Facial Flash Recovery Mask brand=Dr. Brandt Skincare>, 
                                           <Product product_id=1 pr_name=Black Cleansing Oil brand=Erborian>], 
                                           ['Dr. Brandt Skincare', 'Erborian', 'boscia', 'TOM FORD', 'Shiseido'], 
                                           ['Face Wash & Cleansers', 'Face Masks', 'Face Sunscreen', 'Moisturizers'], 
                                           ('ingredient', 'category', 'product', 'brand'), 
                                           [<Ingredient ingredient_id=152 ing_name=Water>, 
                                           <Ingredient ingredient_id=19 ing_name=Carbomer>, 
                                           <Ingredient ingredient_id=100 ing_name=Panthenol>, 
                                           <Ingredient ingredient_id=139 ing_name=Tocopherol>, 
                                           <Ingredient ingredient_id=55 ing_name=Polyquaternium-7>, 
                                           <Ingredient ingredient_id=107 ing_name=Serine>, 
                                           <Ingredient ingredient_id=101 ing_name=Stearic Acid>, 
                                           <Ingredient ingredient_id=45 ing_name=Alanine>, 
                                           <Ingredient ingredient_id=80 ing_name=Betaine>, 
                                           <Ingredient ingredient_id=114 ing_name=Acrylates Copolymer>, 
                                           <Ingredient ingredient_id=116 ing_name=Algae Extract>, 
                                           <Ingredient ingredient_id=147 ing_name=Aluminum Distearate>, 
                                           <Ingredient ingredient_id=16 ing_name=Sodium Citrate>, 
                                           <Ingredient ingredient_id=35 ing_name=Polysorbate 60>, 
                                           <Ingredient ingredient_id=85 ing_name=Polysorbate 80>], 
                                           ['Water', 'Carbomer', 'Panthenol', 'Tocopherol', 'Polyquaternium-7', 'Serine', 'Stearic Acid', 'Alanine', 'Betaine', 'Acrylates Copolymer', 'Algae Extract', 'Aluminum Distearate', 'Sodium Citrate', 'Polysorbate 60', 'Polysorbate 80'])


    def test_search_by_term_2(self):
        """tests search_by_term function"""

        assert search_by_term("boscia") == ([<Product product_id=5 pr_name=Oxygen Facial Flash Recovery Mask brand=Dr. Brandt Skincare>, 
                                            <Product product_id=1 pr_name=Black Cleansing Oil brand=Erborian>, 
                                            <Product product_id=2 pr_name=Radiant Moisture Souffle  brand=TOM FORD>, 
                                            <Product product_id=3 pr_name=Sake Bright White Mask brand=boscia>, 
                                            <Product product_id=4 pr_name=Sports BB Broad Spectrum SPF 50+ WetForce brand=Shiseido>], ['boscia', 'Erborian', 'Dr. Brandt Skincare', 'Shiseido', 'TOM FORD'], ['Face Masks', 'Face Sunscreen', 'Moisturizers', 'Face Wash & Cleansers'], ('brand', 'ingredient', 'product', 'category'), [<Ingredient ingredient_id=4 ing_name=Silica>, <Ingredient ingredient_id=54 ing_name=Ribose>, <Ingredient ingredient_id=16 ing_name=Sodium Citrate>, <Ingredient ingredient_id=109 ing_name=Mica>, <Ingredient ingredient_id=25 ing_name=Isostearic Acid>, <Ingredient ingredient_id=134 ing_name=Sodium Pca>, <Ingredient ingredient_id=15 ing_name=Potassium Sorbate>, <Ingredient ingredient_id=83 ing_name=Capric Acid>, <Ingredient ingredient_id=103 ing_name=Isododecane>, <Ingredient ingredient_id=112 ing_name=Citric Acid>, <Ingredient ingredient_id=81 ing_name=Kaolin>, <Ingredient ingredient_id=99 ing_name=Coco-Betaine>, <Ingredient ingredient_id=101 ing_name=Stearic Acid>, <Ingredient ingredient_id=107 ing_name=Serine>, <Ingredient ingredient_id=8 ing_name=Linoleic Acid>], 
                                            ['Silica', 'Ribose', 'Sodium Citrate', 'Mica', 'Isostearic Acid', 'Sodium Pca', 'Potassium Sorbate', 'Capric Acid', 'Isododecane', 'Citric Acid', 'Kaolin', 'Coco-Betaine', 'Stearic Acid', 'Serine', 'Linoleic Acid'])


    def test_search_by_term_3(self):
        """tests search_by_term function"""

        assert search_by_term(input) == output


    def test_search_by_term_4(self):
        """tests search_by_term function"""

        assert search_by_term(input) == output




if __name__ = "__main__":
    unittest.main()


