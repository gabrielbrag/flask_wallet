from flask import Flask, request, jsonify
import json
from services.accounts_manager import Accounts_manager, AccountNotFoundException, TransactionDataException

app = Flask(__name__)

event_types = ["deposit", 'withdraw']
accounts_manager = Accounts_manager()
   
@app.route('/reset', methods=["POST"])
def reset_api():
    global accounts_manager
    accounts_manager = Accounts_manager()
    return "OK", 200
   
@app.route('/balance')
def get_balance():
    try:
        if request.args.get('account_id'):
            balance = accounts_manager.get_account_balance(int(request.args.get('account_id')))
        else:
            return "0", 404
    except AccountNotFoundException:
        return "0", 404
    
    return str(balance), 200
        
@app.route('/event', methods=['POST'])
def post_event():
    json_dict = request.get_json()    

    origin = None
    if "origin" in json_dict:
        origin = int(json_dict["origin"])

    destination = None
    if "destination" in json_dict:
        destination = int(json_dict["destination"])

    return_data = {}
    return_string = ""
    
    try:
        return_data = accounts_manager.event(event_type=json_dict["type"], destination=destination, value=json_dict["amount"], origin=origin)
        return_string = jsonify(return_data)
        return_code = 201
        
    except AccountNotFoundException:
        return_code = 404
        return_string = '0'
    except TransactionDataException as ex:
        return_string = str(ex)
        return_code = 400
    except Exception as ex:
        print(ex)
        return_code = 400
    
    return return_string, return_code

if __name__ == '__main__':
    app.run()