# test_app.py

import pytest
import json
from frontend import app as frontend_app
from esb import app as esb_app
from service_notification import app as notification_app
from service_payment import app as payment_app

@pytest.fixture
def client():
    app = frontend_app.test_client()
    yield app

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Microservice Control Panel' in response.data

def test_enqueue_request(client):
    response = client.post('/esb', json={"service": "order", "payload": {"order_id": "123"}})
    assert response.status_code == 202
    assert b'Request added to queue' in response.data

def test_status(client):
    response = client.get('/esb/status')
    assert response.status_code == 200
    assert b'queue_size' in response.data
