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

Example Response:

```
{
    "products": [
        {
            "id": "303693660",
            "title": "Peperami Pep'd Up Chicken Bites 50G",
            "category": "Fresh Food",
            "price": 1.0,
            "clubcard_price": 0.75,
            "img_src": "https://digitalcontent.api.tesco.com/v2/media/ghs/06432b37-5464-448a-805c-4d453c902152/ae3d67e9-fb84-4aa1-bf96-464726261750.jpeg?h=540&w=540"
        }
    ]
}
```
