from tkinter import *
import tkinter.ttk as table
import hashlib as hash
import pickle
from datetime import datetime
import tkinter.messagebox as dialog
import people
import helper

FILE_NAME = "files/transaction.ltms"
INDEX_FILE_NAME = "files/transaction_index.txt"


class Transaction:
    def __init__(self, trans_id, person_name, person_id, des, amount, trans_date, trans_type):
        self.id = trans_id
        self.person_name = person_name
        self.person_id = person_id
        self.description = des
        self.amount = amount
        self.date = trans_date
        self.type = "Debit" if trans_type == 0 else "Credit"

    def get_table_data(self, v=None):
        if v != None:
            return self.date, self.id, self.person_name, self.amount
        return self.person_name, self.amount, self.type, self.description, self.date


def get_person_transactions(person):
    transactions = []
    for trans in TRANSACTIONS:
        if trans.person_id == person.id:
            transactions.append(trans)
    return transactions


def remove_person_transactions(person):
    global TRANSACTIONS
    transactions = []
    for trans in TRANSACTIONS:
        if trans.person_id != person.id:
            transactions.append(trans)
    TRANSACTIONS = transactions
    helper.write_transactions(transactions, FILE_NAME)


def get_frame(window):
    frame = Frame(window)

    trans_table = table.Treeview(frame)
    trans_table.grid(row=0, column=0, columnspan=6)
    trans_table["columns"] = ["name", "amount", "type", "des", "dot"]
    trans_table["show"] = "headings"
    trans_table.heading("name", text="Name")
    trans_table.heading("amount", text="Amount")
    trans_table.heading("type", text="Type")
    trans_table.heading("dot", text="Date Of Transaction")
    trans_table.heading("des", text="Description")

    helper.refresh_table(trans_table, TRANSACTIONS)

    add_button = Button(frame, text="Add Transaction",
                        command=lambda: add_transaction(trans_table))
    delete_button = Button(frame, text="Delete Transaction",
                           command=lambda: delete_transaction(trans_table.item(trans_table.selection()[0]),
                                                              trans_table))

    add_button.grid(row=1, column=1, columnspan=2)
    delete_button.grid(row=1, column=3, columnspan=2)

    return frame


def delete_transaction(item, trans_table):
    delete_id = item["tags"][0]
    delete_index = 0
    for i in range(len(TRANSACTIONS)):
        if TRANSACTIONS[i].id == delete_id:
            delete_index = i
            break
    deleted_transaction = TRANSACTIONS[delete_index]
    result = dialog.askquestion("Delete Transaction",
                                "Do you want to delete the Transaction with {} from History?".format(
                                    deleted_transaction.person_name), icon='warning')
    if result == 'yes':
        TRANSACTIONS.pop(delete_index)
        helper.write_transactions(TRANSACTIONS, FILE_NAME)
        dialog.showinfo("Deletion Successful",
                        "The Transaction with person named {} on {} has been deleted from the record.".format(
                            deleted_transaction.person_name, deleted_transaction.date))
        people.change_balance(deleted_transaction.person_id,
                              -deleted_transaction.amount if deleted_transaction.type == "Credit" else deleted_transaction.amount)
        helper.refresh_table(trans_table, TRANSACTIONS)


def update_transactions(old_id, new_id):
    for trans in TRANSACTIONS:
        if trans.person_id == old_id:
            trans.person_id = new_id
    helper.write_transactions(TRANSACTIONS, FILE_NAME)


# Adds a transaction to file.
def add_transaction(trans_table, insert_tran=None):
    # Saving Transactions into File
    def save_transaction(insert_tran=None):
        if insert_tran is None:
            sender_name = people_choices.item(
                people_choices.selection()[0])['values'][0]
            sender_id = str(people_choices.item(
                people_choices.selection()[0])['tags'][0])
            amount = amount_input.get()
            des = des_input.get()
            trans_type = typeOfTrans.get()
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            # Verifying entered Amount
            if not helper.is_amount_valid(amount):
                dialog.showerror("Invalid Input", "Enter Some Amount")
            else:
                # Asking for Confirmation
                r = dialog.askquestion("Insert Transaction",
                                       "Do you want to add this Transaction to record?", icon='warning')
                if r == "yes":
                    amount = int(amount)
                    trans_id = hash.md5(
                        (sender_id + str(amount) + dt_string).encode()).hexdigest()
                    trans = Transaction(
                        trans_id, sender_name, sender_id, des, amount, dt_string, trans_type,)
                    people.change_balance(
                        sender_id, -amount if trans_type == 1 else amount)
                    with open(FILE_NAME, "ab") as file:
                        with open(INDEX_FILE_NAME, "a") as index:
                            index.write(trans_id + " " +
                                        str(file.tell()) + "\n")
                        pickle.dump(trans, file)
                    TRANSACTIONS.append(trans)
                    TRANSACTIONS.sort(
                        key=lambda a_trans: a_trans.date, reverse=True)
                    helper.refresh_table(trans_table, TRANSACTIONS)
                trans_sub_window.destroy()
                helper.refresh_table(trans_table, TRANSACTIONS)
        else:
            people.change_balance(insert_tran.person_id,
                                  insert_tran.amount if insert_tran.type == "Debit" else -insert_tran.amount)
            with open(FILE_NAME, "ab") as file:
                with open(INDEX_FILE_NAME, "a") as index:
                    index.write(insert_tran.id + " " + str(file.tell()) + "\n")
                pickle.dump(insert_tran, file)
            TRANSACTIONS.append(insert_tran)
            TRANSACTIONS.sort(key=lambda a_trans: a_trans.date, reverse=True)
            helper.refresh_table(trans_table, TRANSACTIONS)

    if insert_tran is not None:
        save_transaction(insert_tran)
        return

    # Transaction Window
    trans_sub_window = Tk()
    trans_sub_window.title("Add Transaction")

    bottom_frame = Frame(trans_sub_window)
    bottom_frame.pack(side=BOTTOM)

    add_button = Button(bottom_frame, text="Add Transaction",
                        command=lambda: save_transaction())
    cancel_button = Button(bottom_frame, text="Cancel",
                           command=trans_sub_window.quit)
    add_button.grid(row=6, column=0, columnspan=2)
    cancel_button.grid(row=6, column=2, columnspan=2)

    top_frame = Frame(trans_sub_window)
    top_frame.pack(side=TOP)

    # Adding The Labels And Input Fields (Entry)
    sname = Label(top_frame, text="Sender Name")
    sname.grid(row=0, column=0)

    people_choices = table.Treeview(top_frame)
    people_choices.grid(row=0, column=0, columnspan=2)
    people_choices["columns"] = ["name", "phone"]
    people_choices["show"] = "headings"
    people_choices.heading("name", text="Name")
    people_choices.heading("phone", text="Phone")
    index = 0
    for person in people.PEOPLE:
        people_choices.insert("", index, values=(
            person.name, person.phone), tags=person.id)
        index += 1

    amount = Label(top_frame, text="Amount (in ₹)")
    amount.grid(row=1, column=0)
    amount_input = Entry(top_frame)
    amount_input.grid(row=1, column=1)

    trans_type = Label(top_frame, text="Transaction Type")
    trans_type.grid(row=4, column=0)
    trans_type_frame = Frame(top_frame)
    typeOfTrans = IntVar(trans_type_frame)
    typeOfTrans.set(0)
    debit_radio = Radiobutton(
        trans_type_frame, text="Send", value=0, variable=typeOfTrans)
    credit_radio = Radiobutton(
        trans_type_frame, text="Request", value=1, variable=typeOfTrans)
    debit_radio.pack(side=LEFT)
    credit_radio.pack(side=LEFT)
    trans_type_frame.grid(row=4, column=1)

    des = Label(top_frame, text="Description")
    des.grid(row=5, column=0)
    des_input = Entry(top_frame)
    des_input.grid(row=5, column=1)

    trans_sub_window.mainloop()


TRANSACTIONS = helper.read_transactions(FILE_NAME)
