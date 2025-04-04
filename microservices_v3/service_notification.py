from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notification', methods=['POST'])
def send_notification():
    data = request.json
    order_id = data.get("order_id")
    return jsonify({"message": f"Notification sent for order {order_id}"}), 200

if __name__ == "__main__":
    app.run(port=5003, debug=True)
