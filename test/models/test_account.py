import pytest
import sys
import os

# Made to prevent changes in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from api_ebanx.models.account import Account, Accounts_manager

def test_get_inexistent_account():
    accounts_manager = Accounts_manager()
    test_account = accounts_manager.get_account(330)
    assert test_account == None
    
def test_create_account():
    account = Account(id = 120, balance = 300)
    
    assert account != None
    
def test_create_account_with_invalid_data():
    with pytest.raises(Exception) as ex:
        account = Account(balance = 300)
    with pytest.raises(Exception) as ex:
        account = Account(id = 20)
        
def test_deposit():
    account = Account(id = 120, balance = 300)
    account.event(type='deposit', value=150)
    assert account.balance == 450

def test_invalid_deposit():
    account = Account(id = 120, balance = 300)
    with pytest.raises(Exception) as ex:
        account.event(type='deposit', value=-150)
    
def test_withdraw():
    account = Account(id = 120, balance = 130)
    account.event(type='withdraw', value=40)
    assert account.balance == 90
    
def test_invalid_withdraw():
    account = Account(id = 120, balance = 300)
    with pytest.raises(Exception) as ex:
        account.event(type='withdraw', value=-40)
        
def test_invalid_operation():
    account = Account(id = 120, balance = 300)
    with pytest.raises(Exception) as ex:
        account.event(type='invalid operation', value=300)