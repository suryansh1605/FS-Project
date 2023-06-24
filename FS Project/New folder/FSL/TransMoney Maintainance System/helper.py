import re as regex
import pickle
import os
import people

# A lambda function to check if the email address passed is valid or not.
isEmailValid = lambda email: True if email == "" else regex.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)

# A method to check if a given date is valid.
def isDateValid(date):
    if date == "":
        return True
    isLeapYear = lambda year: (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
    try:
        dates = list(map(int, date.split("/")))
        if dates[1] == 2:
            if isLeapYear(dates[2]) and dates[0] in range(1, 30):
                return True
            elif (not isLeapYear) and dates[0] in range(1, 29):
                return True
            else:
                return False
        elif dates[1] in [1, 3, 5, 7, 8, 10, 12] and dates[0] in range(1, 32):
            return True
        elif dates[1] not in [1, 3, 5, 7, 8, 10, 12] and dates[0] in range(1, 31):
            return True
        else:
            return False
    except:
        return False

def is_amount_valid(amount):
    if amount == "":
        return False
    elif not amount.isdigit():
        return False
    elif int(amount) == 0:
        return False
    else:
        return True

# A method to check if the passed phone number is valid or not.
def isPhoneValid(phone):
    if phone == "":
        return False
    if phone[0] not in ['6', '7', '8', '9']:
        return False
    elif len(phone) != 10:
        return False
    elif not phone.isdigit():
        return False
    else:
        return True

# Returns the list of people.
def read_people(people_file_name, people_index_file_name):
    people_names = []
    try:
        with open(people_file_name, "rb") as people_file, open(people_index_file_name, "r") as index_file:    
            while True:
                line = index_file.readline()
                if line == "":
                    break
                data = eval(line)
                people_file.seek(data[1])
                person = pickle.load(people_file)
                people_names.append(person)
    except EOFError:
        pass
    return people_names

# Returns the list of people.
def write_people(people_list, people_file_name, people_index_file_name):
    indices = {}
    with open(people_file_name, "wb") as people_file, open(people_index_file_name, "w") as index_file:    
        for person in people_list:
            index = people_file.tell()
            data = tuple([person.id, index])
            indices[data[0]] = data[1]
            pickle.dump(person, people_file)
            index_file.write(str(data) + "\n")
    return indices

# Refreshes the table to reflect changes.
def refresh_table(table, data):
    for entry in table.get_children():
        table.delete(entry)
    index = 0
    for entry in data:
        table.insert("", index, values=entry.get_table_data(), tags=entry.id)
        index += 1

def load_indices(people_file_name, people_index_file_name):
    indices = {}
    try:
        with open(people_index_file_name, "r") as file:
            while True:
                line = file.readline()
                if line == "":
                    break
                data = eval(line)
                indices[data[0]] = data[1]
    except EOFError:
        pass
    except FileNotFoundError:
        if not os.path.exists("files"):
            os.mkdir("files")
        with open(people_file_name, "wb") as _, open(people_index_file_name, "w") as _:
            pass
    return indices
            
def read_transactions(transaction_file_name):
    transactions = []
    try:
        with open(transaction_file_name, "rb") as file:
            while True:
                transactions.append(pickle.load(file))
    except EOFError:
        pass
    except FileNotFoundError:
        if not os.path.exists("files"):
            os.mkdir("files")
        with open(transaction_file_name, "wb") as _:#, open(transaction.INDEX_FILE_NAME, "w") as _:
            pass
    transactions.sort(key = lambda a_trans: a_trans.date, reverse = True)
    return transactions 

def write_transactions(transactions, transaction_file_name):
    with open(transaction_file_name, "wb") as file:
        for trans in transactions:
            pickle.dump(trans, file)
