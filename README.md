# TescoPrice

Python API to grab price data from the Tesco website.

Example requests:

Search by product ID

localhost:5000/?id=12345678 

Search with query

localhost:5000/search?query=pepsi 

Search by category

localhost:5000/category?query=bakery

*Note

Categories must be one of the following:
'fresh-food', 'bakery', 'frozen-food', 'food-cupboard', 'drinks', 'baby', 'health-and-beauty', 'pets', 'household'
