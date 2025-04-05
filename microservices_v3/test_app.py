import pytest
import json
from frontend import app as frontend_app
from esb import app as esb_app
from service_notification import app as notification_app
from service_payment import app as payment_app

@pytest.fixture(scope='module')
def client():
    """ Создаем тестовый клиент для фронтенда """
    frontend_app.config['TESTING'] = True
    with frontend_app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def esb_client():
    """ Создаем тестовый клиент для ESB сервиса """
    esb_app.config['TESTING'] = True
    with esb_app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def notification_client():
    """ Создаем тестовый клиент для Notification сервиса """
    notification_app.config['TESTING'] = True
    with notification_app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def payment_client():
    """ Создаем тестовый клиент для Payment сервиса """
    payment_app.config['TESTING'] = True
    with payment_app.test_client() as client:
        yield client

def test_index(client):
    """ Тестируем главную страницу фронтенда """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Microservice Control Panel' in response.data

def test_enqueue_request(esb_client):
    """ Тестируем очередь запросов в ESB сервисе """
    response = esb_client.post('/esb', json={"service": "order", "payload": {"order_id": "123"}})
    assert response.status_code == 202
    assert b'Request added to queue' in response.data

def test_status(esb_client):
    """ Тестируем получение статуса очереди в ESB сервисе """
    response = esb_client.get('/esb/status')
    assert response.status_code == 200
    assert b'queue_size' in response.data

def test_notification_service(notification_client):
    """ Тестируем отправку уведомлений в сервисе Notification """
    response = notification_client.post('/notification', json={"order_id": "123"})
    assert response.status_code == 200
    assert b'Notification sent for order' in response.data

def test_payment_service(payment_client):
    """ Тестируем обработку платежей в сервисе Payment """
    response = payment_client.post('/payment', json={"order_id": "123"})
    assert response.status_code == 200
    assert b'Payment for order processed' in response.data
