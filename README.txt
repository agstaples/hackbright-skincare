# Gadget

## Summary

**Gadget** is an app that allows users to search for skin care products and alerts them if those products contain any potentially harmful or otherwise undesirable ingredients. The app comes loaded with 2 flags: one for ingredients that are potentially harmful during pregnancy and one for environmental pollutants. Users can also create their own custom flags and can diable and enable flags as they please.

## About the Developer

Gadget was created by Anne Staples, a software engineer in Oakland, CA. Learn more about Anne at [LinkedIn](https://www.linkedin.com/in/anne-staples
).

## Technologies

**Tech Stack:**

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- HTML
- CSS
- Javascript
- JQuery
- AJAX
- JSON
- Bootstrap

Gadget is a single-page app built on a Flask server with a PostgreSQL database and utilizing SQLALchemy for object-relational mapping and the Marshmallow library for object serialization. The front end is built with HTML, CSS, some Bootstrap, and Javascript using JQuery and AJAX. The search functionality is bolstered by the Fuzzywuzzy library doing approximate string matching.

## Deeper Dive

I scraped the data for my app from Sephora. There was no API to work with so I used their site map to get individual product page urls and then scraped the product pages for the information I needed for my products table, then I used the ingredient lists from each product to populate my ingredients table.

The ingredient data was a little messy so I did some normalizing with regular expressions to clean them up as much as I could.

There are two built in flags on the app, one for pregnancy and one for environmental pollutants, and then users can create as many custom flags as they want. Because ingredient names are not standardized and the spellings can be tricky, I used a library called fuzzywuzzy to do approximate string matching to show users close ingredient matches that they can add to their flag or not. So any ingredient that matches 99 or 100 percent gets added automatically, and anything between 85 and 98 percent gets alerted to the user for confirmation.

I also used fuzzywuzzy to order search results on the first search results page. So results are organized into categories, brands, products and ingredients. And I used the matching scores to determine in what order those groupings are displayed. 

The database is made up of four main tables (products, ingredients, flags, users) with many to many relationships between them through three join tables (product ingredients, ingredient flags, user flags)

I used a library called Marshmallow to set up schemas for serializing my response objects so I could easily turn them into json to pass to my front end.

And I set up methods on my schemas so for any product object I can call it’s associated flags and whether those flags are enabled or disabled since users can enable and disable flags as they please.

So on the front end it allows me to display all the product information in each product card, and then any enabled flag data in the banner.

And if the user wants easy visibility into which products are free from any ingredients they are flagging, they can just switch off the flagged products by clicking the Gadget logo in the top left on the navbar and easily click through to Sephora to purchase the product they want.

## Next Steps

- **Slackbot:** Set up a Slackbot that you can ping with a product name and brand and it will respond with any flag information
- **Testing:** Implement more testing
- **Refactoring:** Reduce the number of queries I am currently making on my database