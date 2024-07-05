from flask import Flask, request, jsonify
import json
from models.account import Account, Accounts_manager

app = Flask(__name__)

event_types = ["deposit", 'withdraw']
accounts_manager = Accounts_manager()

@app.route('/')
def get_home():
   return "hello world"
   
@app.route('/balance')
def get_balance():
    get_response = accounts_manager.get_account(request.args.get('account_id'))
    
    if get_response == None:
        return "Account not found", 404
    return json.dumps(get_response)

@app.route('/event', methods=['POST'])
def post_event():
    posted_json = request.get_json()    

    json_dict = json.loads(posted_json)   

    # Validate required fields
    required_fields = ["destination", "amount", "type"]
    if not all(field in json_dict for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Additional validation logic if needed (e.g., type checks)
    valid_event_types = ["deposit", "withdraw"]  # Example valid types
    if json_dict["type"] not in valid_event_types:
        return jsonify({"error": "Invalid event type"}), 400
    
    get_response = accounts_manager.get_account(json_dict["destination"])

    if get_response == None:

        new_account = Account(id = json_dict["destination"], balance = json_dict["amount"])
        accounts_manager.add_account(new_account)
        
        return_data = { "destination":{} }
        return_data["destination"]["id"] = new_account.id
        return_data["destination"]["balance"] = new_account.balance
        
        return_code = 201
        
    return jsonify(return_data), return_code

if __name__ == '__main__':
    app.run(debug=True)