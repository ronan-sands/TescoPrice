from flask import request
from flask import Response
import json
import scrape

categories = ['fresh-food', 'bakery', 'frozen-food', 'food-cupboard', 'drinks', 'baby', 'health-and-beauty', 'pets', 'household']
def make_response(r):
        response = Response(response=r, status=200, mimetype='application/json')
        response.headers["Content-Type"]="application/json"
        response.headers["Access-Control-Allow-Origin"]="*"
        return response
def configure(app):
    @app.route('/search')
    def search():
        query = request.args.get('query')
        products = scrape.getProductsFromSearch(query)
        
        try: 
            jsonArr = scrape.productsToJsonArray(products)
            return make_response(jsonArr)
        except Exception as e:
            print(e)
            return error_response(500)

    @app.route('/category')
    def category():
        category = request.args.get('query')
        if(not category in categories):
            return error_response(404)
        products = scrape.getProductsFromCategory(category)
        try: 
            jsonArr = scrape.productsToJsonArray(products)
            return make_response(jsonArr)
        except Exception as e:
            print(e)
            return error_response(500)
    @app.route('/')
    def by_id():
        id = request.args.get('id')
        products = scrape.getProductById(id)
        if(products==None):
            return no_products_response()
        try: 
            jsonArr = scrape.productsToJsonArray(products)
            return make_response(jsonArr)
        except Exception as e:
            print(e)
            return error_response(500)
def error_response(code):
        r = {
            "error": True,
            "message": "Unknown Error Occurred",
            "status_code": code
            }
        if(code==404):
            r["message"] = "Error: Bad Request"
        if(code==500):
            r["message"] = "Error: Internal Server Error"
        reply = json.dumps(r)
        response = Response(response=reply, status=code, mimetype='application/json')
        response.headers["Content-Type"]="application/json"
        response.headers["Access-Control-Allow-Origin"]="*"
        return response

def no_products_response():
    r = {
        "message" : "No Products Found"
    }
    reply = json.dumps(r)
    response = Response(response=reply, status=200, mimetype='application/json')
    response.headers["Content-Type"]="application/json"
    response.headers["Access-Control-Allow-Origin"]="*"
    return response
