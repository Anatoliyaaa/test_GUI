from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/order', methods=['GET'])
def seb():
    return "This is the /sdasda"

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    order_id = data.get("order_id")
    return jsonify({"message": f"Order {order_id} created successfully"}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
