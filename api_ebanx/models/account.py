

event_types = ["deposit", 'withdraw']

class Account():
    def __init__(self, id, balance):       
        self.id        = id
        self.balance   = balance
                
    def event(self, type, value):
        if type not in event_types:
            raise ValueError("invalid operation type")
        
        if value <= 0:
            raise ValueError("event value must be greater than 0")
        
        if type == 'deposit':
            self.balance += value
        if type == 'withdraw':
            self.balance -= value
            
class Accounts_manager:
    def __init__(self) -> None:
        self.accounts = []
        
    def get_account(self, account_id):
        for account in self.accounts:
            if account["id"] == account_id:
                return account
        return None  # Account not found in the list
    
    def add_account(self, account):
        self.accounts.append(account)