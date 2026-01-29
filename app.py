from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from database import get_db

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ------------------ PRODUCTS ------------------

@app.route("/products", methods=["GET"])
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    return jsonify(data)

@app.route("/add-product", methods=["POST"])
def add_product():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, quantity) VALUES (%s,%s,%s)",
        (data["name"], data["price"], data["quantity"])
    )
    db.commit()
    socketio.emit("inventory_updated")
    return jsonify({"message": "Product Added"})

@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE products SET quantity = quantity - %s WHERE id = %s",
        (data["quantity"], data["product_id"])
    )
    db.commit()
    socketio.emit("inventory_updated")
    return jsonify({"message": "Order Created"})

# ------------------ RUN ------------------

if __name__ == "__main__":
    socketio.run(app, debug=True)
