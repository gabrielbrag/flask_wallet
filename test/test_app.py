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
    assert response.text == "0"
    
def test_get_balance_without_account(client):
    response = client.get('/balance')
    assert response.status_code == 404
    assert response.text == "0"
      
def test_create_new_account_and_make_deposit(client):
    response = client.post('/event', json={"type":"deposit", "destination":"100", "amount":10})
    assert response.status_code == 201
    assert response.json == {"destination": {"id": "100", "balance": 10}}

def test_make_deposit_existing_account(client):
    response = client.post('/event', json={"type":"deposit", "destination":"100", "amount":30})
    assert response.status_code == 201
    assert response.json == {"destination": {"id": "100", "balance": 40}}

def test_post_with_invalid_data(client):
    response = client.post('/event', json={"type":"deposit", "amount":10})
    assert response.status_code == 400
    
    response = client.post('/event', json={"type":"invalid operation", "destination":"100", "amount":10})
    assert response.status_code == 400
    
    response = client.post('/event', json={"type":"deposit", "destination":"100"})
    assert response.status_code == 400
    
def test_get_balance_existing_account(client):
    response = client.get('/balance?account_id=100')
    assert response.status_code == 200  
    assert response.text == '40'
    
def test_withdraw_from_non_existing_account(client):
    response = client.post('/event', json={"type":"withdraw", "amount":10, "origin":325})
    assert response.status_code == 404
    assert response.text == '0'
    
def test_withdraw_from_existing_account(client):
    response_from_get = client.get('/balance?account_id=100')
    
    response = client.post('/event', json={"type":"withdraw", "origin":"100", "amount":10})
    assert response.status_code == 201
    
    expected_balance = float(response_from_get.text) - 10
    
    assert response.json == {"origin": {"id": "100", "balance": expected_balance}}
    
def test_transfer_from_existing_account(client):
    response_from_get = client.get('/balance?account_id=100')
    expected_balance = float(response_from_get.text) + 10
    
    #Creates a new account
    client.post('/event', json={"type":"deposit", "amount":45, "destination":200})
    
    response = client.post('/event', json={"type":"transfer", "origin":200, "destination":"100", "amount":10})
    
    assert response.status_code == 201
    assert response.json == {"origin": {"id":"200", "balance":35}, "destination": {"id":"100", "balance":expected_balance}}
    
# def test_transfer_to_a_non_existing_account(client):
#     #When transfer to a non-existing account, the account should be created
    
def test_transfer_from_non_existing_account(client):       
    response = client.post('/event', json={"type":"transfer", "origin":299, "destination":"100", "amount":10})
    
    assert response.status_code == 404
    assert response.text == '0'
    
def test_transfer_to_non_existing_account(client):
    response = client.post('/event', json={"type":"transfer", "origin":100, "destination":"674", "amount":10})
    
    assert response.status_code == 201
    assert response.json == {'destination': {'balance': 10, 'id': '674'}, 'origin': {'balance': 30, 'id': '100'}}
    
def test_reset(client):
    response = client.get('/balance?account_id=100')
    assert response.status_code != 404 #Assert that the accounts still exists
    
    response = client.post('/reset') #Reset API
    assert response.status_code == 200
    assert response.text == "OK"
    
    response = client.get('/balance?account_id=100') #Assert that account ceased to exist
    assert response.status_code == 404
    assert response.text == "0"