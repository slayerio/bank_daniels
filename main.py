import account_info
import os
from datetime import datetime

bank_accounts = account_info.bank_accounts


def save_accounts_to_file():
    with open('account_info.py', 'w') as f:
        f.write('bank_accounts = {\n')
        for acc_num, acc_details in bank_accounts.items():
            f.write(f'    {acc_num}: {{\n')
            f.write(f'        "first_name": "{acc_details["first_name"]}",\n')
            f.write(f'        "last_name": "{acc_details["last_name"]}",\n')
            f.write(f'        "id_number": "{acc_details["id_number"]}",\n')
            f.write(f'        "balance": {acc_details["balance"]:.2f},\n')

            # Write transaction history
            f.write('        "transaction_history": [\n')
            for transaction in acc_details["transaction_history"]:
                f.write(f'            {transaction},\n')
            f.write('        ],\n')

            # Write transactions to execute
            f.write('        "transactions_to_execute": [\n')
            for transaction in acc_details["transactions_to_execute"]:
                f.write(f'            {transaction},\n')
            f.write('        ],\n')

            f.write('    },\n')
        f.write('}\n')

    print("Accounts updated and saved to 'account_info.py'.")


def account_ver():
    process_scheduled_transactions()
    print("welcome to bank daniel's. before continuing, we will have to verify your account")
    while True:
        try:
            acc_number = int(input("enter your account number. if you don't remember it - enter 2 to register by id"
                                   "if you don't have an account - enter 0"))

            if acc_number == 2:
                id_verification = input("enter your id")

                # a while loop to narrow id to 9 digit only
                while True:
                    if not id_verification.isdigit() or len(id_verification) != 9:
                        print("id not valid, enter id containing 9 numbers only")
                        id_verification = (input("enter your id"))
                    else:
                        break

                for key, value in bank_accounts.items():
                    if value["id_number"] == id_verification:
                        if value["id_number"] == '000000000':
                            another_verification = input("enter your account number")
                            if another_verification == '1000':
                                print("hello manager!")
                                menu(1000)
                                return
                            else:
                                print("invalid manager account number")
                                continue
                        print(f"Hello {value['first_name']} {value['last_name']}!")
                        menu(key)  # the key = acc_number
                        return

                print("ID not found. Please try again.")
            elif not acc_number:
                new_account()
            else:
                for key, value in bank_accounts.items():
                    if key == acc_number:
                        if key == 1000:
                            another_verification_id = input("enter your id number")
                            if another_verification_id == '000000000':
                                print("hello manager!")
                                menu(1000)
                                return
                            else:
                                print("invalid manager id")
                                continue

                        print(f"hello{bank_accounts[key]["first_name"], bank_accounts[key]["last_name"]}!")
                        menu(acc_number)
                        return
                    continue
                not_found = int(input("account not found. press 1 to try again, press 2 to open a new account"))
                match not_found:
                    case 1:
                        continue
                    case 2:
                        new_account()
                        return
        except ValueError:
            print("not valid number")


def new_account():
    print("welcome to bank_daniels!")
    new_account_number = max(bank_accounts.keys()) + 1
    first_name = input("what's your first name?")
    last_name = input("what's your last name?")
    while True:
        id_number = input("Enter your ID number(9 numbers): ")
        if not id_number.isdigit() or len(id_number) != 9:
            print("id not valid, enter id containing 9 numbers only")
            continue
        elif any(acc['id_number'] == id_number for acc in bank_accounts.values()):
            print("This ID number already exists. Please enter a different ID number.")
        else:
            break
    while True:
        try:
            balance = float(input("what's your exact balance?"))
            break
        except ValueError:
            print("enter a valid number")

    bank_accounts[new_account_number] = {
        "first_name": first_name,
        "last_name": last_name,
        "id_number": id_number,
        "balance": balance,
        "transactions_to_execute": [],
        "transaction_history": []
    }

    print(f"Account created successfully! Your account number is {new_account_number}.")
    print(bank_accounts[new_account_number])

    menu(new_account_number)

    save_accounts_to_file()


def menu(acc_number):
    while True:
        if acc_number == 1000:
            print("to see accounts report - enter 0")
            print("to see transactions_to_execute - enter 1")
            print("to see transaction_history - enter 2")
            print("to exit - enter 9")

            manager_choice = input("")
            match manager_choice:
                case "0":
                    acc_report(acc_number)
                case "1":
                    transaction_report()
                case "2":
                    transaction_history(acc_number)
                case "9":
                    print("have a good day")
                case _:
                    print("Invalid option, please try again.")
        else:
            print("to check your balance - enter 1")
            print("to make a transaction - enter 2")
            print("to check transaction history - enter 3")
            print("for account report - enter 4")
            print("to exit - enter 9")

            choice = input("")
            match choice:
                case "1":
                    check_balance(acc_number)
                case "2":
                    make_transaction(acc_number)
                case "3":
                    check_transaction(acc_number)
                case "4":
                    acc_report(acc_number)
                case "9":
                    print("have a good day, thanks for choosing Bank Daniel's(™)")
                    return
                case _:
                    print("Invalid option, please try again.")


def acc_report(acc_number):
    # Report for a specific account
    if acc_number in bank_accounts and acc_number != 1000:
        print(f"Account Number: {acc_number}")
        print(f"First Name: {bank_accounts[acc_number]['first_name']}")
        print(f"Last Name: {bank_accounts[acc_number]['last_name']}")
        print(f"Balance: {bank_accounts[acc_number]['balance']}")
        print("Transaction History:")
        for transaction in bank_accounts[acc_number]["transaction_history"]:
            print(transaction)
        print("Transactions to Execute:")
        for transaction in bank_accounts[acc_number]["transactions_to_execute"]:
            print(transaction)

    # Special report for management account (account 1000)
    elif acc_number == 1000:
        for key, value in bank_accounts.items():  # Use .items() to iterate over both key and value
            print(f"Account Number: {key}")
            print(f"First Name: {value['first_name']}")
            print(f"Last Name: {value['last_name']}")
            print(f"Balance: {value['balance']}")
            print("Transaction History:")
            for transaction in value["transaction_history"]:
                print(transaction)
            print("Transactions to Execute:")
            for transaction in value["transactions_to_execute"]:
                print(transaction)
            print()


def check_balance(acc_number):
    balance = bank_accounts[acc_number]['balance']
    print(f"Your current balance is: ${balance:.2f}")


def transaction_history(acc_number):
    if acc_number == 1000:
        for key, value in bank_accounts.items():
            for transaction in value["transaction_history"]:
                print(transaction)


def make_transaction(acc_number):
    while True:
        try:
            recipient_acc_number = int(input("Enter recipient's account number: "))
            if recipient_acc_number not in bank_accounts:
                print("recipient's account numbers are invalid.")
                continue

            amount = float(input("Enter the amount to transfer: "))
            # Check if the sender has sufficient balance
            if bank_accounts[acc_number]["balance"] < amount:
                print("Insufficient balance.")
                continue

            transaction_time = input("enter 1 to make the transaction, enter 2 to make a future transaction")
            match transaction_time:
                case '1':
                    bank_accounts[acc_number]["balance"] -= amount
                    bank_accounts[recipient_acc_number]["balance"] += amount

                    # Record the transaction in both accounts' transaction history
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    bank_accounts[acc_number]["transaction_history"].append(
                        (timestamp, acc_number, recipient_acc_number, amount, "Transfer Sent")
                    )
                    bank_accounts[recipient_acc_number]["transaction_history"].append(
                        (timestamp, acc_number, recipient_acc_number, amount, "Transfer Received")
                    )
                    save_accounts_to_file()
                    print(f"Successfully transferred {amount} from Account {acc_number} to Account {recipient_acc_number}.")
                case '2':
                    scheduled_time = input("when would you like to make the transaction? %Y-%m-%d %H:%M:%S")
                    schedule_transaction(acc_number, str(recipient_acc_number), amount,scheduled_time)
            return
        except ValueError:
            print("Invalid input. Please enter correct values.")
            continue


def schedule_transaction(acc_number: str, recipient_acc_number: str, amount: float, scheduled_time):
    if acc_number in bank_accounts:
        # Add the new transaction to the "transactions_to_execute" for the specified account
        bank_accounts[acc_number]["transactions_to_execute"].append(
            {"recipient": recipient_acc_number, "amount": amount, "scheduled_time": scheduled_time}
        )
        print(f"Transaction scheduled from Account {acc_number} to {recipient_acc_number} for {scheduled_time}.")
    else:
        print(f"Account {acc_number} not found.")

    # Write back the updated bank_accounts dictionary to account_info.py
    with open('account_info.py', 'w') as file:
        file.write(f"bank_accounts = {bank_accounts}\n")


def process_scheduled_transactions():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for acc_number, account_data in bank_accounts.items():
        for transaction in account_data["transactions_to_execute"]:
            if transaction["scheduled_time"] <= current_time:
                recipient_acc_number = transaction["recipient"]
                amount = transaction["amount"]

                # Process the transaction
                bank_accounts[acc_number]["balance"] -= amount
                bank_accounts[recipient_acc_number]["balance"] += amount

                # Add to transaction history of both accounts
                bank_accounts[acc_number]["transaction_history"].append(
                    (current_time, acc_number, recipient_acc_number, amount, "Transfer Sent")
                )
                bank_accounts[recipient_acc_number]["transaction_history"].append(
                    (current_time, acc_number, recipient_acc_number, amount, "Transfer Received")
                )

                # Remove the transaction from transactions_to_execute
                account_data["transactions_to_execute"].remove(transaction)

                print(f"Processed scheduled transaction of {amount} from {acc_number} to {recipient_acc_number}.")

    # After processing, write the updated data back to account_info.py
    with open('account_info.py', 'w') as file:
        file.write(f"bank_accounts = {bank_accounts}\n")


def check_transaction(acc_number):
    try:
        transaction_history = bank_accounts[acc_number]["transaction_history"]

        # Check if the account has any transaction history
        if not transaction_history:
            print(f"Account {acc_number} has no transaction history.")
            return

        # Display the transaction history
        print(f"\nTransaction History for Account {acc_number}:")
        for transaction in transaction_history:
            print(
                f"Date: {transaction[0]}, From: {transaction[1]},"
                f" To: {transaction[2]}, Amount: {transaction[3]}, Status: {transaction[4]}")

    except ValueError:
        print("Invalid account number. Please try again.")


def transaction_report():
    for key, value in bank_accounts.items():
        print(f"Account Number: {key}")
        print("Transactions to Execute:")
        for transaction in value["transactions_to_execute"]:
            print(transaction)
        print()


account_ver()
