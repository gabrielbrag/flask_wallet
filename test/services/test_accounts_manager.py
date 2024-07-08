import pytest
import sys
import os

# Made to prevent changes in PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir) + '../../api_ebanx')

from api_ebanx.models.account import Account
from api_ebanx.services.accounts_manager import Accounts_manager, AccountNotFoundException, TransactionDataException

@pytest.fixture
def manager():
    return Accounts_manager()

def test_add_account_and_check_balance(manager):
    test_account = Account(id = 1, balance = 10)
    manager.add_account(test_account)
    
    assert len(manager.accounts) == 1
    
    balance = manager.get_account_balance(account_id = 1)    
    assert balance == 10
    
def test_check_inexistent_account_balance(manager):
    with pytest.raises(AccountNotFoundException) as ex:
        manager.get_account_balance(account_id=1000)

def test_mandatory_transaction_fields(manager):
    #Deposit without value
    with pytest.raises(TransactionDataException) as ex:
        manager.event(event_type="deposit", destination=2, value=0, origin=None) 

    #Deposit without destination
    with pytest.raises(TransactionDataException) as ex:
        manager.event(event_type="deposit", destination=0, value=100, origin=None) 
        
    #Do a invalid transaction
    with pytest.raises(TransactionDataException) as ex:
        manager.event(event_type="invalid transaction", destination=30, value=100, origin=None) 

def test_deposit_existing_account(manager):
    #Creating account
    manager.event(event_type = "deposit", destination = 1, value = 10, origin=None)

    #Makes deposit into it
    manager.event(event_type = "deposit", destination = 1, value = 20, origin=None)
    balance = manager.get_account_balance(account_id = 1)
    
    assert balance == 30 #10 from creation + 20 from deposit   
    
def test_withdraw_event(manager):
    manager.event(event_type = "deposit", destination = 1, value = 10, origin=None)
    
    manager.event(event_type = "withdraw", origin = 1, value = 20, destination=None)
    balance = manager.get_account_balance(account_id = 1)
    
    assert balance == -10 #10 from creation - 20 from withdraw, 
    #for this implementation considered that the balance could be negative
    
def test_transfer_event_between_existing_accounts(manager):
    manager.event(event_type = "deposit", destination = 1, value = 100, origin=None)
    manager.event(event_type = "deposit", destination = 2, value = 10, origin=None)

    balance_of_account_1 = manager.get_account_balance(account_id = 1)
      
    response_data = manager.event(event_type="transfer", destination=2, value=50, origin=1)
    
    assert response_data["origin"]["balance"] == 50 #100 from creation - 50 from transfer
    assert response_data["destination"]["balance"] == 60 #10 from created account + 50 from transfer
    
def test_transfer_event_to_non_existing_account(manager):
    manager.event(event_type = "deposit", destination = 1, value = 150, origin=None)
    
    response_data = manager.event(event_type="transfer", destination=20, value=50, origin=1)
    
    assert response_data["origin"]["balance"] == 100 #150 from creation - 50 from transfer
    assert response_data["destination"]["balance"] == 50
    
def test_invalid_transfer(manager):
    #Transfer without origin 
    with pytest.raises(TransactionDataException) as ex:
        manager.event(event_type="transfer", value=50, destination=2, origin=None)