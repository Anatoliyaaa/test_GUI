from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/payment', methods=['POST'])
def process_payment():
    data = request.json
    order_id = data.get("order_id")
    return jsonify({"message": f"Payment for order {order_id} processed"}), 200

if __name__ == "__main__":
    app.run(port=5002, debug=True)
