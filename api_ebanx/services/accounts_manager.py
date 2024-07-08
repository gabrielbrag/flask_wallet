            
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
                
    def event(self, event_type:str, destination:int, value:float, **kwargs) -> any:        
        if event_type == '':
            raise TransactionDataException("event_type could not be empty")
        
        if destination == 0:
            raise TransactionDataException("destination could not be empty")
        
        if value == 0:
            raise TransactionDataException("the value of the transaction could not be 0")
        
        valid_event_types = ["deposit", "withdraw", "transfer"] 
        if event_type not in valid_event_types:
            raise TransactionDataException("invalid event type")
        
        origin_account = None
        
        try:
            destination_account = self.get_account(destination)
            
        except AccountNotFoundException:
            if event_type in ("withdraw", "transfer"):
                error_message = "withdraw from" if event_type == "withdraw" else "transfer to"
                raise AccountNotFoundException("could not " + error_message + " an inexisting account")
            else:
                destination_account = Account(id = destination, balance = value)
                self.add_account(destination_account)
        else:
            if (event_type == "transfer"):
                origin_id = kwargs.get("origin")
                try:
                    origin_account = self.get_account(origin_id)
                    origin_account.event("withdraw", value)
                    destination_account.event("deposit", value)
                except AccountNotFoundException:
                    raise AccountNotFoundException("origin account not found")
            else:   
                destination_account.event(event_type, value)
        
        return_data = { "destination":{} }
        return_data["destination"]["id"]        = str(destination_account.id)
        return_data["destination"]["balance"]   = destination_account.balance
        
        if origin_account != None:
            return_data["origin"] = {}
            return_data["origin"]["id"]         = str(origin_account.id)
            return_data["origin"]["balance"]    = origin_account.balance
                    
        return return_data