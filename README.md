# Wallet management API
This API provides a simple interface to manage wallets and bank accounts, developed as part of a Python engineer selection process.

# Language and framework choice
For this project, developers were given the freedom to choose their preferred programming language. I opted for Python due to its flexibility and alignment with the position's requirements.

To keep the project straightforward, I selected the Flask framework for its ease of setup and minimalistic approach. The project's file structure and architecture were designed to reflect simplicity, minimizing the number of classes and dependencies.

# Overview of the project structure

## Models/account.py
This file contains a basic model for accounts, comprising an ID and a balance. Transactions are limited to withdrawals and deposits. Although the API specification included a third transaction type, "transfer," I implemented an orchestrator class to manage transfers separately. This approach ensures that account objects are only aware of their own operations.

## Services/accounts_manager.py
Central to the API, this class orchestrates transactions. It maintains a list of accounts and handles operations by instantiating and invoking account objects as necessary. Transfers are managed by debiting one account and crediting another. To adhere to the API specification, which excludes persistence requirements, data is stored in memory as an attribute of the class. The structure is designed to facilitate future integration of persistence mechanisms if needed.

## App.py
The entry point for the Flask project, this file defines the web routes for the service. It utilizes the AccountsManager class to handle the user transactions.
