

event_types = ["deposit", 'withdraw']

class Account():
    def __init__(self, id:str, balance:float) -> None:       
        self.id        = id
        self.balance   = balance
                
    def event(self, type:str, value:float) -> None:
        if type not in event_types:
            raise ValueError("invalid operation type")
        
        if value <= 0:
            raise ValueError("event value must be greater than 0")
        
        if type == 'deposit':
            self.balance += value
        if type == 'withdraw':
            self.balance -= value