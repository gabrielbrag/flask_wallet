import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../api_ebanx')))


from api_ebanx.app import app as flask_app

@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })

    yield flask_app

    
@pytest.fixture()
def client(app):
    return app.test_client()

def test_get_balance_inexistent_account(client):
    response = client.get('/balance?account_id=1')
    assert response.status_code == 404
  
def test_create_new_account(client):
    response = client.post('/event', json='{"type":"deposit", "destination":"100", "amount":10}')
    assert response.status_code == 201
    assert response.json == {"destination": {"id": "100", "balance": 10}}
 
def test_post_with_invalid_data(client):
    response = client.post('/event', json='{"type":"deposit", "amount":10}')
    assert response.status_code == 400
    
    response = client.post('/event', json='{"type":"invalid operation", "destination":"100", "amount":10}')
    assert response.status_code == 400
    
    response = client.post('/event', json='{"type":"deposit", "destination":"100"}')
    assert response.status_code == 400
