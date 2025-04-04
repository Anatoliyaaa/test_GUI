from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

ESB_URL = "http://localhost:5000/esb"
ESB_STATUS_URL = "http://localhost:5000/esb/status"

@app.route('/', methods=['GET', 'POST'])
def index():
    response_data = None

    if request.method == 'POST':
        service = request.form.get('service')
        order_id = request.form.get('order_id')
        payload = {"order_id": order_id}

        try:
            esb_response = requests.post(ESB_URL, json={"service": service, "payload": payload})
            response_data = esb_response.json()
        except Exception as e:
            response_data = {"error": str(e)}

    return render_template("index.html", response=response_data)

@app.route('/status')
def status():
    try:
        status_response = requests.get(ESB_STATUS_URL)
        return jsonify(status_response.json())
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=5004, debug=True)
