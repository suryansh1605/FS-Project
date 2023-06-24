from tkinter import *
import transaction
import people
import tkinter.ttk as table
from datetime import datetime

def get_frame(window):
    frame = Frame(window, name = "dashboard")

    now = datetime.now()
    date_string = now.strftime("%d %B %Y")

    date = Label(frame, text = date_string, borderwidth = 2, padx = 5, pady = 5)
    date.grid(row = 0, column = 0, columnspan = 6, rowspan = 1)

    pay_money_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)
    recieve_money_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)
    transactions_card = Frame(frame, borderwidth = 2, relief = "raised", padx = 5, pady = 5)

    give, get = people.get_total_balance_dashboard()
    give_text = Label(pay_money_card, text = "Pay ₹" + str(give))
    give_text.pack()
    get_text = Label(recieve_money_card, text = "Receive ₹" + str(get))
    get_text.pack()

    trans_table = table.Treeview(transactions_card)
    trans_table.grid(row = 0, column = 0, columnspan = 6)
    trans_table["columns"] = ["name", "amount", "type", "des", "dot"]
    trans_table["show"] = "headings"
    trans_table.heading("name", text = "Name")
    trans_table.heading("amount", text = "Amount")
    trans_table.heading("type", text = "Type")
    trans_table.heading("dot", text = "Date Of Transaction")
    trans_table.heading("des", text = "Description")
    index = 0
    for trans in transaction.TRANSACTIONS[:5]:
        trans_table.insert("", index, values=(trans.person_name, trans.amount, trans.type, trans.description, trans.date))
        index += 1
    pay_money_card.grid(row = 1, column = 0, columnspan = 3, rowspan = 2)
    recieve_money_card.grid(row = 1, column = 3, columnspan = 3, rowspan = 2)
    transactions_card.grid(row = 3, column = 1, columnspan = 4, rowspan = 2)

    return frame