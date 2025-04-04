from flask import Flask, request, jsonify
import requests
import threading
import queue
import time

app = Flask(__name__)

request_queue = queue.Queue()
processed_requests = []

service_urls = {
    "order": "http://localhost:5001/order",
    "payment": "http://localhost:5002/payment",
    "notification": "http://localhost:5003/notification"
}


def worker():
    while True:
        item = request_queue.get()
        if item is None:
            break

        service = item['service']
        payload = item['payload']
        try:
            print(f"Processing request to {service} with payload: {payload}")
            time.sleep(2)  # имитация задержки
            response = requests.post(service_urls[service], json=payload)
            processed_requests.append({
                "service": service,
                "payload": payload,
                "response": response.json(),
                "status": response.status_code
            })
        except requests.exceptions.RequestException as e:
            processed_requests.append({
                "service": service,
                "payload": payload,
                "error": str(e)
            })
        request_queue.task_done()


# запускаем поток-обработчик
threading.Thread(target=worker, daemon=True).start()


@app.route('/')
def index():
    return "ESB with Queue is running!", 200


@app.route('/esb', methods=['POST'])
def enqueue_request():
    data = request.json
    service = data.get("service")
    payload = data.get("payload", {})

    if service not in service_urls:
        return jsonify({"error": f"Service '{service}' not found"}), 400

    request_queue.put({
        "service": service,
        "payload": payload
    })

    return jsonify({"message": "Request added to queue"}), 202


@app.route('/esb/status', methods=['GET'])
def status():
    return jsonify({
        "queue_size": request_queue.qsize(),
        "processed": processed_requests[-10:]  # последние 10
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
