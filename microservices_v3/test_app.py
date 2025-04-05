import pytest
from unittest.mock import MagicMock

# Заглушки для приложения Flask (мы не будем запускать реальные сервисы)
@pytest.fixture(scope='module')
def frontend_app():
    """ Заглушка для фронтенд приложения """
    app = MagicMock()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope='module')
def esb_app():
    """ Заглушка для ESB сервиса """
    app = MagicMock()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope='module')
def notification_app():
    """ Заглушка для Notification сервиса """
    app = MagicMock()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope='module')
def payment_app():
    """ Заглушка для Payment сервиса """
    app = MagicMock()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope='module')
def client():
    """ Заглушка для тестового клиента фронтенда """
    mock_client = MagicMock()
    mock_client.get.return_value.status_code = 200
    mock_client.get.return_value.data = b'Microservice Control Panel'
    yield mock_client

@pytest.fixture(scope='module')
def esb_client():
    """ Заглушка для тестового клиента ESB """
    mock_client = MagicMock()
    mock_client.post.return_value.status_code = 202
    mock_client.post.return_value.data = b'Request added to queue'
    yield mock_client

@pytest.fixture(scope='module')
def notification_client():
    """ Заглушка для тестового клиента Notification """
    mock_client = MagicMock()
    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.data = b'Notification sent for order'
    yield mock_client

@pytest.fixture(scope='module')
def payment_client():
    """ Заглушка для тестового клиента Payment """
    mock_client = MagicMock()
    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.data = b'Payment for order processed'
    yield mock_client

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
