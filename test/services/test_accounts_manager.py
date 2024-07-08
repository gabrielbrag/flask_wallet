import pytest
import sys
import os

# Made to prevent changes in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from api_ebanx.models.account import Account
from api_ebanx.services.accounts_manager import Accounts_manager, AccountNotFoundException, TransactionDataException

#Global manager used in all tests
manager = Accounts_manager()

def test_add_account_and_check_balance():
    test_account = Account(id = 1, balance = 10)
    manager.add_account(test_account)
    
    assert len(manager.accounts) == 1
    
    balance = manager.get_account_balance(account_id = 1)    
    assert balance == 10
    
def test_check_inexistent_account_balance():
    with pytest.raises(AccountNotFoundException) as ex:
        manager.get_account_balance(account_id=1000)

def test_mandatory_transaction_fields():
    #Deposit without value
    with pytest.raises(TransactionDataException) as ex:
        manager.event(event_type="deposit", destination=2, value=0) 

    #Deposit without destination
    with pytest.raises(TransactionDataException) as ex:
        manager.event(event_type="deposit", destination=0, value=100) 
        
    #Do a invalid transaction
    with pytest.raises(TransactionDataException) as ex:
        manager.event(event_type="invalid transaction", destination=30, value=100) 

def test_deposit_event():
    current_balance = manager.get_account_balance(account_id = 1)        
    manager.event(event_type = "deposit", destination = 1, value = 20)
    balance = manager.get_account_balance(account_id = 1)
    
    assert balance == (current_balance + 20)    
    
def test_withdraw_event():
    current_balance = manager.get_account_balance(account_id = 1)
    manager.event(event_type = "withdraw", destination = 1, value = 10)
    balance = manager.get_account_balance(account_id = 1)
    
    assert balance == (current_balance - 10)
    
def test_transfer_event():
    #Creating a new account
    manager.event(event_type = "deposit", destination = 2, value = 350)
    
    current_balance = manager.get_account_balance(account_id = 1)
    
    response_data = manager.event(event_type="transfer", destination=1, value=50, origin=2)
    
    assert response_data["origin"]["balance"] == 300
    assert response_data["destination"]["balance"] == current_balance + 50
    
def test_invalid_transfer():
    #Transfer without origin 
    with pytest.raises(AccountNotFoundException) as ex:
        manager.event(event_type="transfer", value=50, destination=2)