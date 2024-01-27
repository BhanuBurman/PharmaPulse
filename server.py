from flask import Flask,jsonify,request
from flask.helpers import send_from_directory
from flask_cors import CORS,cross_origin


from Web_Scrapper.Scrapper import search_products
app = Flask(__name__, static_folder="client/build", static_url_path="")
CORS(app)

@app.route('/products',methods = ['GET'])
@cross_origin()
def products():
    medicine_name = request.args.get('medicine', '')
    products_list = search_products(medicine_name)
    
    # Extract relevant information for demonstration (change as needed)
    response_data = {i: [
        {
            'name': product.name,
            'img':product.image_url,
            'link': product.link,
            'price': product.price,
            'offer_price': product.offer_price
        } for product in scrapper_results
    ] for i, scrapper_results in enumerate(products_list)}

    return jsonify({'products': response_data})

@app.route("/")
@cross_origin()
def serve():
    return send_from_directory(app.static_folder,"index.html")

if __name__ == '__main__':
    app.run(debug=True)