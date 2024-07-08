            
from models.account import Account

class AccountNotFoundException(Exception):
    pass

class TransactionDataException(Exception):
    pass

class Accounts_manager:
    def __init__(self) -> None:
        self.accounts = []
        
    def get_account(self, account_id:int) -> Account:
        for account in self.accounts:
            if account.id == account_id:
                return account
        raise AccountNotFoundException("Account not found")
    
    def add_account(self, account:Account):
        self.accounts.append(account)
    
    def get_account_balance(self, account_id:int):
        account = self.get_account(account_id)
        return account.balance
    
    def validate_transaction(self, event_type:str, destination:int, value:float, origin:int):
        if not event_type:
            raise TransactionDataException("event_type could not be empty")
        
        if (value is None or value == 0):
           raise TransactionDataException("the value of the transaction could not be 0")
                       
        valid_event_types = ["deposit", "withdraw", "transfer"] 
        if event_type not in valid_event_types:
            raise TransactionDataException("invalid event type")

        if not destination and not origin:
            raise TransactionDataException("destination or origin must be provided")

        if event_type == "transfer" and (not destination or not origin):
            raise TransactionDataException("Both origin and destination must be provided for a transfer")       
       
               
    def event(self, event_type:str, destination:int, value:float, origin:int):
        self.validate_transaction(event_type, destination, value, origin)

        origin_account = None
        destination_account = None

        try:
            if origin:
                origin_account = self.get_account(origin)
        except AccountNotFoundException:
            raise AccountNotFoundException("origin account not found")
        
        try:
            if destination:
                destination_account = self.get_account(destination)
        except AccountNotFoundException:
            destination_account = Account(id = destination, balance = 0)
            self.add_account(destination_account)

        if (event_type == "transfer"):
            origin_account.event("withdraw", value)
            destination_account.event("deposit", value)
        else:
            if destination_account:
                destination_account.event(event_type, value)
            if origin_account:
                origin_account.event(event_type, value)
        
        return_data = {}
        
        if destination_account:
            return_data["destination"] = {
                "id": str(destination_account.id),
                "balance": destination_account.balance
            }
            
        if origin_account:
            return_data["origin"] = {
                "id": str(origin_account.id),
                "balance": origin_account.balance
            }
                    
        return return_data