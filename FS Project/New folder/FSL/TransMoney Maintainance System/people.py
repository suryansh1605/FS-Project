from tkinter import *
import tkinter.messagebox as dialog
from tkinter.simpledialog import askstring
import tkinter.ttk as table
import hashlib as hash
import pickle
from datetime import datetime
import helper
import transaction
import smtplib
import os
from email.message import EmailMessage
import ssl

FILE_NAME = "files/people.ltms"
INDEX_FILE_NAME = "files/people_index.txt"


# A Person class to store the details of a person.
class Person:
    # The constructor of the class.
    def __init__(self, person_id, name, email, phone, address, gender, dob, balance=0):
        self.id = person_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.gender = gender
        self.dob = dob
        self.balance = balance

    # Returns the Data of the person.
    def get_data(self):
        return [
            ("Name", self.name),
            ("Phone Number", self.phone),
            ("Email Address", self.email),
            ("Balance", "You have to {} ₹{}".format("give" if self.balance < 0 else "receive", abs(self.balance))),
            ("Address", self.address),
            ("Gender", "Male" if self.gender == 0 else "Female" if self.gender == 1 else "Other"),
            ("Date of Birth", self.dob)
        ]

    # Returns a tuple having the name, phone and email of the person.
    def get_table_data(self):
        return self.name, self.phone, self.email

    # Returns a frame containing the key-value pair of information of the person.
    def get_data_frame(self, window):
        frame = Frame(window, borderwidth=2, relief="raised")
        details_table = table.Treeview(frame)
        details_table["columns"] = ["parameter", "value"]
        details_table["show"] = "headings"
        index = 0
        for data in self.get_data():
            details_table.insert("", index, values=data)
            index += 1
        details_table.grid(row=0, column=0, columnspan=3)
        return frame


def get_total_balance_dashboard():
    give, get = 0, 0
    for person in PEOPLE:
        if person.balance < 0:
            give += abs(person.balance)
        else:
            get += person.balance
    return give, get


def search_person(people_table):
    person_phone = askstring("Search", "Enter Phone Number")
    status = False
    if person_phone != None:
        for people in PEOPLE:
            if people.phone == person_phone:
                view_person(people.id, people_table, True)
                status = True
        if not status:
            dialog.showerror("Not Found", "There exists no person with the phone number {}".format(person_phone))



# This method takes in the main window of the program as a parameter and generates and returns the frame of the Person Module.
def get_frame(window):
    frame = Frame(window, name="people")

    # Table to display the people.
    people_table = table.Treeview(frame)
    people_table.grid(row=0, column=0, columnspan=4)
    people_table["columns"] = ["name", "phone", "email"]
    people_table["show"] = "headings"
    people_table.heading("name", text="Name")
    people_table.heading("email", text="Email Address")
    people_table.heading("phone", text="Phone Number")

    helper.refresh_table(people_table, PEOPLE)

    # Buttons to add, modify and delete a person.
    add_button = Button(frame, text="Add Person", command=lambda: add_person(people_table))
    search_button = Button(frame, text="Search by Phone", command=lambda: search_person(people_table))
    view_button = Button(frame, text="View Details",
                         command=lambda: view_person(people_table.item(people_table.selection()[0]), people_table))
    delete_button = Button(frame, text="Delete",
                           command=lambda: delete_person(people_table.item(people_table.selection()[0]), people_table))

    add_button.grid(row=1, column=0)
    search_button.grid(row=1, column=1)
    view_button.grid(row=1, column=2)
    delete_button.grid(row=1, column=3)

    return frame


# Opens a window displaying the information and the recent transactions of the person.
def view_person(item, people_table, direct=False):
    person_id = str(item["tags"][0]) if not direct else item
    person = get_person(INDICES[person_id])

    person_details_window = Tk()
    transactions_frame = Frame(person_details_window)

    trans_table = table.Treeview(transactions_frame)
    trans_table.grid(row=0, column=0, columnspan=4)
    trans_table["columns"] = ["dot", "amount", "type", "des"]
    trans_table["show"] = "headings"
    trans_table.heading("amount", text="Amount")
    trans_table.heading("type", text="Type")
    trans_table.heading("dot", text="Date Of Transaction")
    trans_table.heading("des", text="Description")
    index = 0
    for trans in transaction.get_person_transactions(person):
        trans_table.insert("", index, values=(trans.date, trans.amount, trans.type, trans.description))
        index += 1
    transactions_frame.grid(row=0, column=0, columnspan=2)
    person_frame = person.get_data_frame(person_details_window)
    person_frame.grid(row=0, column=2, columnspan=2)
    edit_button = Button(person_frame, text="Edit", command=lambda: add_person(people_table, person))
    edit_button.grid(row=1, column=0)
    clear_balance_button = Button(person_frame, text="Clear Balance",
                                  command=lambda: clear_balance(person, trans_table, person_details_window))
    clear_balance_button.grid(row=1, column=1)
    close_button = Button(person_frame, text="Close", command=person_details_window.destroy)
    close_button.grid(row=1, column=2)
    person_details_window.mainloop()


def get_person(index):
    with open(FILE_NAME, "rb") as file:
        file.seek(index)
        return pickle.load(file)


def clear_balance(person, trans_table, person_details_window):
    if abs(person.balance) == 0:
        dialog.showerror("Error","Balance is Already Zero")
    else:
        result = dialog.askquestion("Clear Balance",
                                "Do you want to clear the balance of ₹{} of {}?".format(abs(person.balance),
                                                                                        person.name), icon='warning')
        if result == 'yes':
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            trans_id = hash.md5((person.id + str(-person.balance) + dt_string).encode()).hexdigest()
            trans = transaction.Transaction(trans_id, person.name, person.id, "Clear Balance", abs(person.balance),
                                            dt_string, 1 if person.balance > 0 else 0)
            transaction.add_transaction(trans_table, trans)
            person_details_window.destroy()


# This method deletes the selected item from the people table.
def delete_person(item, people_table):
    global PEOPLE, INDICES
    delete_id = str(item["tags"][0])
    print(delete_id)
    print("-----------------------------------------------------")
    delete_index = -1
    for i in range(len(PEOPLE)):
        print(type(PEOPLE[i].id), type(delete_id))
        if PEOPLE[i].id == delete_id:
            print()
            delete_index = i
            break
    deleted_person = PEOPLE[delete_index]
    result = dialog.askquestion("Delete Person", "Do you want to delete {} from contacts?".format(deleted_person.name),
                                icon='warning')
    if result == 'yes':
        PEOPLE.pop(delete_index)
        INDICES = helper.write_people(PEOPLE, FILE_NAME, INDEX_FILE_NAME)
        dialog.showinfo("Deletion Successful",
                        "The person named {} has been deleted from the record.".format(deleted_person.name))
        helper.refresh_table(people_table, PEOPLE)
        r = dialog.askquestion("Delete Transactions",
                               "Do you want to delete the transactions related to {}".format(deleted_person.name),
                               icon='warning')
        if r == "yes":
            transaction.remove_person_transactions(deleted_person)


# Changes the balance of the person.
def change_balance(person_id, amount):
    global PEOPLE, INDICES
    for person in PEOPLE:
        if person.id == person_id:
            person.balance += amount
            print(person.balance)
            break
    INDICES = helper.write_people(PEOPLE, FILE_NAME, INDEX_FILE_NAME)


# This method is used to add a person.
def add_person(people_table, edit_person=None):
    # This method saves the person to the file.
    def save_person(edit):
        global INDICES, PEOPLE

        person_name = name_input.get()
        person_email = email_input.get()
        person_phone = phone_input.get()
        person_address = address_input.get("1.0", "end-1c")
        person_gender = gender_int.get()
        person_dob = dob_input.get()
        hash_string = (person_name + person_phone)
        person_id = hash.md5(hash_string.encode()).hexdigest()

        person = Person(person_id, person_name, person_email, person_phone, person_address, person_gender, person_dob,
                        edit_person.balance if edit_person is not None else 0)

        if person_name == "":
            dialog.showerror("Invalid Input", "Name cannot be empty.")
        elif not helper.isPhoneValid(person_phone):
            dialog.showerror("Invalid Input", "Invalid Phone Number.")
        elif not helper.isEmailValid(person_email):
            dialog.showerror("Invalid Input", "Invalid Email.")
        elif not helper.isDateValid(person_dob):
            dialog.showerror("Invalid Input", "Invalid Date of Birth.")
        elif edit:
            if edit_person.id != person_id and person_id in INDICES:
                dialog.showerror("Duplicate Entry", "Person already exists.")
                return
            result = dialog.askquestion("Confirm Changes", "Do you want to save changes?", icon='warning')
            if result == 'yes':
                for i in range(len(PEOPLE)):
                    if PEOPLE[i].id == edit_person.id:
                        PEOPLE[i] = person
                        break
                INDICES = helper.write_people(PEOPLE, FILE_NAME, INDEX_FILE_NAME)
                transaction.update_transactions(edit_person.id, person.id)
                PEOPLE.sort(key=lambda person: person.name)
                person_sub_window.destroy()
                helper.refresh_table(people_table, PEOPLE)
        else:
            for person_id in INDICES.keys():
                if person_id == person.id:
                    dialog.showerror("Duplicate Entry", "Person already exists.")
                    break
            else:
                with open(FILE_NAME, "ab") as file:
                    pickle.dump(person, file)
                    PEOPLE.append(person)
                INDICES = helper.write_people(PEOPLE, FILE_NAME, INDEX_FILE_NAME)
                PEOPLE.sort(key=lambda person: person.name)
                person_sub_window.destroy()
                helper.refresh_table(people_table, PEOPLE)

        Mail_procedure(person_email, person_name)
        
    person_sub_window = Tk()
    person_sub_window.title("Add Person")

    bottom_frame = Frame(person_sub_window)
    bottom_frame.pack(side=BOTTOM)

    save_button = Button(bottom_frame, text="Save", command=lambda: save_person(edit_person is not None))
    cancel_button = Button(bottom_frame, text="Cancel", command=person_sub_window.destroy)
    cancel_button.pack(side=RIGHT)
    save_button.pack(side=RIGHT)

    top_frame = Frame(person_sub_window)
    top_frame.pack(side=TOP)

    name = Label(top_frame, text="Name")
    name.grid(row=0, column=0)
    name_input = Entry(top_frame)
    name_input.insert(END, "" if edit_person is None else edit_person.name)
    name_input.grid(row=0, column=1)

    email = Label(top_frame, text="Email")
    email.grid(row=1, column=0)
    email_input = Entry(top_frame)
    email_input.insert(END, "" if edit_person is None else edit_person.email)
    email_input.grid(row=1, column=1)

    phone = Label(top_frame, text="Phone")
    phone.grid(row=2, column=0)
    phone_input = Entry(top_frame)
    phone_input.insert(END, "" if edit_person is None else edit_person.phone)
    phone_input.grid(row=2, column=1)

    address = Label(top_frame, text="Address")
    address.grid(row=3, column=0)
    address_input = Text(top_frame, width=50, height=4)
    address_input.insert(END, "" if edit_person is None else edit_person.address)
    address_input.grid(row=3, column=1)

    gender = Label(top_frame, text="Gender")
    gender.grid(row=4, column=0)
    gender_int = IntVar(top_frame)

    gender_frame = Frame(top_frame)
    male_radio = Radiobutton(gender_frame, text="Male", value=0, variable=gender_int)
    female_radio = Radiobutton(gender_frame, text="Female", value=1, variable=gender_int)
    other_radio = Radiobutton(gender_frame, text="Other", value=2, variable=gender_int)

    gender_value = 0 if edit_person is None else edit_person.gender
    if gender_value == 0:
        male_radio.select()
    elif gender_value == 1:
        female_radio.select()
    else:
        other_radio.select()

    male_radio.pack(side=LEFT)
    female_radio.pack(side=LEFT)
    other_radio.pack(side=LEFT)
    gender_frame.grid(row=4, column=1)

    dob = Label(top_frame, text="Date of Birth (DD/MM/YYYY)")
    dob.grid(row=5, column=0)
    dob_input = Entry(top_frame)
    dob_input.insert(END, "" if edit_person is None else edit_person.dob)
    dob_input.grid(row=5, column=1)

    person_sub_window.mainloop()


INDICES = helper.load_indices(FILE_NAME, INDEX_FILE_NAME)
PEOPLE = helper.read_people(FILE_NAME, INDEX_FILE_NAME)



def Mail_procedure(person_email , person_name):
    email_sender = 'praveenhegde0987@gmail.com'
    email_password = 'laqpudzqgzdgcpsx'
    email_reciever = person_email
    email_name = person_name

    subject = 'This is the mail from TransMoney'
    body1 = "Haiii  "+ email_name  
    body2 = "This is the checking mail sent from the Trans money banking Sysytem"
    body = body1+body2

    em = EmailMessage()
    em['From']= email_sender
    em['To'] = email_reciever
    em['subject']= subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())

    print("The mail sent")
