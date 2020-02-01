from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

stores = [
    {
        "name": "My Super Store",
        "items": [
            {
                "name": "Item1",
                "price": 19.99
            }
        ]
    }
]


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route("/store")
def get_stores():
    return jsonify({"stores": stores})

@app.route("/store", methods=["POST"])
def create_store(name):
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'], 
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store), 200
    return jsonify({'message': 'Store not found'}), 404

@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({"items": store["items"]}), 200
    return jsonify({'message': 'Store not found'}), 404

@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            request_data = request.get_json()
            new_item = {
                "name": request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store not found'}), 404



app.run(port=5000, debug=True)
