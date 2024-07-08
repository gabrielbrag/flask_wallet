from flask import Flask, request, jsonify
import json
from services.accounts_manager import Accounts_manager, AccountNotFoundException, TransactionDataException

app = Flask(__name__)

event_types = ["deposit", 'withdraw']
accounts_manager = Accounts_manager()
   
@app.route('/balance')
def get_balance():
    try:
        balance = accounts_manager.get_account_balance(request.args.get('account_id'))
    except AccountNotFoundException:
        return "Account not found", 404
    
    return str(balance), 200
        
@app.route('/event', methods=['POST'])
def post_event():
    posted_json = request.get_json()    

    json_dict = json.loads(posted_json)  

    origin = None
    if "origin" in json_dict:
        origin = json_dict["origin"]

    return_data = {}
    return_string = ""
    
    try:
        print(json_dict)
        return_data = accounts_manager.event(event_type=json_dict["type"], destination=json_dict["destination"], value=json_dict["amount"], origin=origin)
        return_string = jsonify(return_data)
        return_code = 201
        
    except AccountNotFoundException:
        return_code = 404
        return_string = '0'
    except TransactionDataException as ex:
        return_string = str(ex)
        return_code = 400
    except Exception:
        return_code = 400
    
    return return_string, return_code

if __name__ == '__main__':
    app.run(debug=True)