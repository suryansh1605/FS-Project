from tkinter import *
import tkinter.ttk as table
import webbrowser as web
import people
import dashboard
import transaction
import passbook


# TODO: Testing the switching between frames (change_frame meethod)

def change_frame(frame, name, prev="None"):
    global window, people_button, transactions_button, passbook_button
    frame.destroy()
    if name == "Dashboard":
        frame = dashboard.get_frame(window)
        frame.pack(side=TOP)
        if prev == "People" or prev == "Transaction" or prev == "Passbook":
            people_button.config(text="People", command=lambda: change_frame(
                frame, "People", "Dashboard"))
            transactions_button.config(text="Transaction",
                                       command=lambda: change_frame(frame, "Transaction", "Dashboard"))
            passbook_button.config(text="Passbook", command=lambda: change_frame(
                frame, "Passbook", "Dashboard"))
            people_button.pack(side=LEFT)
            transactions_button.pack(side=LEFT)
            passbook_button.pack(side=LEFT)

    elif name == "People":
        if prev == "Transaction":
            people_button.config(text="Dashboard", command=lambda: change_frame(
                frame, "Dashboard", "People"))
            transactions_button.config(text="Transaction", command=lambda: change_frame(
                frame, "Transaction", "People"))
            passbook_button.config(
                text="Passbook", command=lambda: change_frame(frame, "Passbook", "People"))
        if prev == "Passbook":
            people_button.config(text="Dashboard", command=lambda: change_frame(
                frame, "Dashboard", "People"))
            transactions_button.config(text="Transaction", command=lambda: change_frame(
                frame, "Transaction", "People"))
            passbook_button.config(
                text="Passbook", command=lambda: change_frame(frame, "Passbook", "People"))
        if prev == "Dashboard":
            people_button.config(text="Dashboard", command=lambda: change_frame(
                frame, "Dashboard", "People"))
            transactions_button.config(
                command=lambda: change_frame(frame, "Transaction", "People"))
            passbook_button.config(
                command=lambda: change_frame(frame, "Passbook", "People"))

        frame = people.get_frame(window)
        frame.pack(side=TOP)

    elif name == "Transaction":
        if prev == "People":
            transactions_button.config(text="Dashboard",
                                       command=lambda: change_frame(frame, "Dashboard", "Transaction"))
            people_button.config(text="People", command=lambda: change_frame(
                frame, "People", "Transaction"))
            passbook_button.config(text="Passbook", command=lambda: change_frame(
                frame, "Passbook", "Transaction"))
        if prev == "Passbook":
            transactions_button.config(text="Dashboard",
                                       command=lambda: change_frame(frame, "Dashboard", "Transaction"))
            people_button.config(text="People", command=lambda: change_frame(
                frame, "People", "Transaction"))
            passbook_button.config(text="Passbook", command=lambda: change_frame(
                frame, "Passbook", "Transaction"))
        if prev == "Dashboard":
            transactions_button.config(text="Dashboard",
                                       command=lambda: change_frame(frame, "Dashboard", "Transaction"))
            people_button.config(command=lambda: change_frame(
                frame, "People", "Transaction"))
            passbook_button.config(command=lambda: change_frame(
                frame, "Passbook", "Transaction"))
        frame = transaction.get_frame(window)
        frame.pack(side=TOP)

    elif name == "Passbook":
        if prev == "People":
            passbook_button.config(text="Dashboard",
                                   command=lambda: change_frame(frame, "Dashboard", "Passbook"))
            transactions_button.config(text="Transaction",
                                       command=lambda: change_frame(frame, "Transaction", "Passbook"))
            people_button.config(text="People", command=lambda: change_frame(
                frame, "People", "Passbook"))
        if prev == "Transaction":
            passbook_button.config(text="Dashboard",
                                   command=lambda: change_frame(frame, "Dashboard", "Passbook"))
            people_button.config(text="People", command=lambda: change_frame(
                frame, "People", "Passbook"))
            transactions_button.config(text="Transaction",
                                       command=lambda: change_frame(frame, "Transaction", "Passbook"))
        if prev == "Dashboard":
            passbook_button.config(text="Dashboard", command=lambda: change_frame(
                frame, "Dashboard", "Passbook"))
            transactions_button.config(command=lambda: change_frame(
                frame, "Transaction", "Passbook"))
            people_button.config(command=lambda: change_frame(
                frame, "People", "Passbook"))
        frame = passbook.get_frame(window)
        frame.pack(side=TOP)


# This method adds the menu to the program.
def add_menu(window):
    menu = Menu(window)
    window.config(menu=menu)

    files_menu = Menu(menu)
    help_menu = Menu(menu)
    tranmethod_menu = Menu(menu)

    files_menu.add_command(label="Exit", command=window.quit)

    about_menu = Menu(help_menu)
    about_menu.add_command(label="Suryansh Kumar Srivastava",
                           command=lambda: web.open("https://www.linkedin.com/in/suryansh-kumar-srivastava-2a1829220/"))
    about_menu.add_command(label="Utkarsh Kumar",
                           command=lambda: web.open("https://www.linkedin.com/in/utkarshkumar190/"))
    about_menu.add_command(label="Praveen N H",
                           command=lambda: web.open("https://www.linkedin.com/in/praveen-hegde-003a80257/"))
    about_menu.add_command(label="Nithin S",
                           command=lambda: web.open("https://www.linkedin.com/in/nithin-seerappa-358506258/"))

    help_menu.add_cascade(label="About", menu=about_menu)

    about_menu = Menu(tranmethod_menu)
    about_menu.add_command(label="UPI Scanner page",
                           command=lambda: web.open("https://suryansh1605.github.io/UPI-Scanner/"))

    tranmethod_menu.add_cascade(label="UPI Scanner", menu=about_menu)

    menu.add_cascade(label="File", menu=files_menu)
    menu.add_cascade(label="Help", menu=help_menu)
    menu.add_cascade(label="Transation Method", menu=tranmethod_menu)


# Main Logic of the function
window = Tk()
window.title("TransMoney Management System")
add_menu(window)
frame = dashboard.get_frame(window)
frame.pack(side=TOP)
navigation_frame = Frame(window)
people_button = Button(navigation_frame, text="People",
                       command=lambda: change_frame(frame, "People", "Dashboard"))
transactions_button = Button(navigation_frame, text="Transactions",
                             command=lambda: change_frame(frame, "Transaction", "Dashboard"))
passbook_button = Button(navigation_frame, text="Passbook",
                         command=lambda: change_frame(frame, "Passbook", "Dashboard"))
quit_button = Button(navigation_frame, text="Quit", command=window.quit)
people_button.pack(side=LEFT)
transactions_button.pack(side=LEFT)
passbook_button.pack(side=LEFT)
quit_button.pack(side=LEFT)
navigation_frame.pack(side=BOTTOM)
window.mainloop()
