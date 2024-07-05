from flask import Flask, request
from models.account import Account

app = Flask(__name__)

@app.route('/')
def get_home():
   return "hello world"
   
def get_balance():
    get_response = Account.get(request.args.get('account_id'))
    return "hello world"