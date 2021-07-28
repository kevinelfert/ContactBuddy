"""
Imports

Need to import
    - tkinter
    - Contact class
    - Database Functions
    - Email Validator module (third party)
    - SQLite3
"""
import tkinter as tk
import Contact.contact as contact
from contact_buddy_db_funcs import save_contact_db, update_contact_db, delete_contact_db
from email_validator import validate_email, EmailNotValidError
import sqlite3

"""
maybe do a dedicated print menu function
"""


"""
Configure the Database
Connect to the database
Create a contacts table (if it does not already exist)
"""
DB_FILENAME = 'contacts.db'

conn = sqlite3.connect(DB_FILENAME)

conn.execute('CREATE table IF NOT EXISTS contacts (first_name text, last_name text, phone_number text, email_address text)')

class ContactBuddy():
    """
    describe contact buddy class
    """
    def __init__(self, main_window):
        """
        constructor

        set the main window to the passed window

        add the title
        add the label
        add the listbox
        fill the listbox
        add the buttons
        """
        self.main_window = main_window
        self.main_window.geometry("450x300")
        self.main_window.configure(background="#5fb3b3")
        self.main_window.title("Contact Buddy")
        self.main_window.protocol("WM_DELETE_WINDOW", self.main_window.destroy)

        self.big_label = tk.Label(self.main_window, text="Contacts")
        self.big_label.configure(background="#5fb3b3")
        self.big_label.config(font=("Arial", 24))
        self.big_label.pack()
        self.contact_listbox = tk.Listbox(self.main_window, selectmode=tk.SINGLE)

        # self.curs = conn.execute('SELECT * FROM contacts')

        self.update_list()

        self.contact_listbox.pack(fill=tk.X, expand=1)

        self.delete_button = tk.Button(self.main_window, text="Delete Contact", command=lambda: self.delete_contact(self.contact_listbox))
        self.delete_button.pack(side=tk.BOTTOM)

        self.modify_button = tk.Button(self.main_window, text="Modify Contact", command=lambda: self.modify_contact(self.contact_listbox))
        self.modify_button.pack(side=tk.BOTTOM)

        self.add_button = tk.Button(self.main_window, text="Add Contact", command=lambda: self.add_contact(self.contact_listbox))
        self.add_button.pack(side=tk.BOTTOM)

    def update_list(self):
        """
        update_list

        This function update the listbox when any data is changed

        first select all from the database in alphabetical order of last name

        delete all the contents of the listbox

        loop through all rows of the contacts table
            -create a contact 
            -add the contact data to the listbox
            -add the contact to a list
        """
        self.curs = conn.execute('SELECT * FROM contacts ORDER BY last_name ASC')

        self.contact_listbox.delete(0, tk.END)
        self.contacts_list = []
        for row in self.curs.fetchall():
            self.c = contact.Contact(row[0], row[1], row[2] , row[3])
            self.contact_listbox.insert(tk.ANCHOR , "Name: "+self.c.get_first()+" "+self.c.get_last()+"\t P: "+self.c.get_phone()+"\t Email: "+self.c.get_email())
            self.contacts_list.append(self.c)

    def add_contact(self, event):
        """
        add_contact

        This function handles the graphical portion of adding a contact
        
        create the form

        on button press, pass the contact data to the add_contact_db function
        """
        second_window = tk.Tk()
        second_window.geometry("450x200")
        second_window.title("Add Contact")
        second_window.configure(background="#5fb3b3")

        #First Name entry box
        first_name_frame = tk.Frame(second_window)
        first_name_frame.pack()
        first_name_label = tk.Label(first_name_frame, text="First Name:")
        first_name_label.config(font=("Arial", 20))
        first_name_label.configure(background="#5fb3b3")
        first_name_label.pack(side=tk.LEFT)
        first_name_entry = tk.Entry(first_name_frame)
        first_name_entry.pack(side=tk.LEFT)

        #Last Name entry box
        last_name_frame = tk.Frame(second_window)
        last_name_frame.pack()
        last_name_label = tk.Label(last_name_frame, text="Last Name:")
        last_name_label.config(font=("Arial", 20))
        last_name_label.configure(background="#5fb3b3")
        last_name_label.pack(side=tk.LEFT)
        last_name_entry = tk.Entry(last_name_frame)
        last_name_entry.pack(side=tk.LEFT)

        #Phone Number entry box
        phone_number_frame = tk.Frame(second_window)
        phone_number_frame.pack()
        phone_number_label = tk.Label(phone_number_frame, text="Phone Number:")
        phone_number_label.config(font=("Arial", 20))
        phone_number_label.configure(background="#5fb3b3")
        phone_number_label.pack(side=tk.LEFT)
        phone_number_entry = tk.Entry(phone_number_frame)
        phone_number_entry.pack(side=tk.LEFT)

        #Phone number format warning
        phone_number_warning_frame = tk.Frame(second_window)
        phone_number_warning_frame.pack()
        phone_number_warning = tk.Label(phone_number_warning_frame, text="(Formatted as 1234567890)")
        phone_number_warning.config(font=("Arial", 12))
        phone_number_warning.configure(background="#5fb3b3")
        phone_number_warning.pack(side=tk.LEFT)

        #email address entry box
        email_address_frame = tk.Frame(second_window)
        email_address_frame.pack()
        email_address_label = tk.Label(email_address_frame, text="Email Address:")
        email_address_label.config(font=("Arial", 20))
        email_address_label.configure(background="#5fb3b3")
        email_address_label.pack(side=tk.LEFT)
        email_address_entry = tk.Entry(email_address_frame)
        email_address_entry.pack(side=tk.LEFT)

        #email address format warning
        email_address_warning_frame = tk.Frame(second_window)
        email_address_warning_frame.pack()
        email_address_warning = tk.Label(email_address_warning_frame, text="(Formatted as user@domain.com)")
        email_address_warning.config(font=("Arial", 12))
        email_address_warning.configure(background="#5fb3b3")
        email_address_warning.pack(side=tk.LEFT)

        #save button
        save_button = tk.Button(second_window, text="Save Contact", command=lambda: self.add_contact_db(first_name_entry.get().strip(), last_name_entry.get().strip(), phone_number_entry.get().strip(), email_address_entry.get().strip(), second_window))
        save_button.pack(side=tk.BOTTOM)

        second_window.mainloop()

    def add_contact_db(self, first_name, last_name, phone_number, email_address, passed_window):
        """
        add_contact_db

        This is the backend function to add a contact

        First, check the email address to see if it is valid
        Then, check the phone number to see if it is valid

        Then, set an error message if there is one

        if there is an error message
            -open a window
            -inform user of the error

        else
            -create the new contact
            -call the add_contact_db function
            -destroy the window containing the form
            -update the listbox
        """
        valid = None
        try:
            valid = validate_email(email_address)
        except:
            pass
            #I know except pass blocks are bad practice
            #I am handling the error in the elif block

        error_message = ""
        if self.validate_phone(phone_number) == False:
            error_message = "Phone Number is not in valid format"  
        elif not valid:
            error_message = "Email Address is not in valid format"

        if error_message != "":
            third_window = tk.Tk()
            third_window.title("Error!")
            third_window.configure(background="#5fb3b3")
            third_window_label = tk.Label(third_window, text=error_message)
            third_window_label.configure(background="#5fb3b3")
            third_window_label.config(font=("Arial", 24))
            third_window_label.pack()
            third_window.geometry("450x100")
        else:
            contact_to_add=contact.Contact(first_name.capitalize(), last_name.capitalize(), phone_number, email_address)
            save_contact_db(contact_to_add)
            passed_window.destroy()
            self.update_list()

    def modify_contact(self, listbox_widget):
        """
        modify_contact

        This function handles the graphical portion of modifying a contact

        if the user has selected an option
            -create the form
            -fill out the entry boxes with preexisting data
            -on button press, pass the new data to the modify_contact_db function

        else
            -create a window with a message informing the user that they must select an option
        """
        second_window = tk.Tk()
        index = listbox_widget.curselection()
        if index:
            contact = self.contacts_list[index[0]]
            second_window.title(contact.get_first()+" "+contact.get_last())
            second_window.geometry("450x200")
            second_window.configure(background="#5fb3b3")

            #First Name entry box
            first_name_frame = tk.Frame(second_window)
            first_name_frame.pack()
            first_name_label = tk.Label(first_name_frame, text="First Name:")
            first_name_label.config(font=("Arial", 20))
            first_name_label.configure(background="#5fb3b3")
            first_name_label.pack(side=tk.LEFT)
            first_name_entry = tk.Entry(first_name_frame)
            first_name_entry.insert(tk.END, contact.get_first())
            first_name_entry.pack(side=tk.LEFT)

            #Last Name entry box
            last_name_frame = tk.Frame(second_window)
            last_name_frame.pack()
            last_name_label = tk.Label(last_name_frame, text="Last Name:")
            last_name_label.config(font=("Arial", 20))
            last_name_label.configure(background="#5fb3b3")
            last_name_label.pack(side=tk.LEFT)
            last_name_entry = tk.Entry(last_name_frame)
            last_name_entry.insert(tk.END, contact.get_last())
            last_name_entry.pack(side=tk.LEFT)

            #Phone Number entry box
            phone_number_frame = tk.Frame(second_window)
            phone_number_frame.pack()
            phone_number_label = tk.Label(phone_number_frame, text="Phone Number:")
            phone_number_label.config(font=("Arial", 20))
            phone_number_label.configure(background="#5fb3b3")
            phone_number_label.pack(side=tk.LEFT)
            phone_number_entry = tk.Entry(phone_number_frame)
            phone_number_entry.insert(tk.END, contact.get_phone())
            phone_number_entry.pack(side=tk.LEFT)

            #Phone number format warning
            phone_number_warning_frame = tk.Frame(second_window)
            phone_number_warning_frame.pack()
            phone_number_warning = tk.Label(phone_number_warning_frame, text="(Formatted as 1234567890)")
            phone_number_warning.configure(background="#5fb3b3")
            phone_number_warning.config(font=("Arial", 12))
            phone_number_warning.pack(side=tk.LEFT)

            #email address entry box
            email_address_frame = tk.Frame(second_window)
            email_address_frame.pack()
            email_address_label = tk.Label(email_address_frame, text="Email Address:")
            email_address_label.config(font=("Arial", 20))
            email_address_label.configure(background="#5fb3b3")
            email_address_label.pack(side=tk.LEFT)
            email_address_entry = tk.Entry(email_address_frame)
            email_address_entry.insert(tk.END, contact.get_email())
            email_address_entry.pack(side=tk.LEFT)

            #email address format warning
            email_address_warning_frame = tk.Frame(second_window)
            email_address_warning_frame.pack()
            email_address_warning = tk.Label(email_address_warning_frame, text="(Formatted as user@domain.com)")
            email_address_warning.config(font=("Arial", 12))
            email_address_warning.configure(background="#5fb3b3")
            email_address_warning.pack(side=tk.LEFT)
            
            #save button
            save_button = tk.Button(second_window, text="Modify Contact", command=lambda: self.modify_contact_db(first_name_entry.get().strip(), last_name_entry.get().strip(), phone_number_entry.get().strip(), email_address_entry.get().strip(), contact, second_window))
            save_button.pack(side=tk.BOTTOM)
        else:
            second_window.title("Error!")
            second_window.configure(background="#5fb3b3")
            second_window_label = tk.Label(second_window, text="You must make a selection")
            second_window_label.config(font=("Arial", 24))
            second_window_label.configure(background="#5fb3b3")
            second_window_label.pack()
            second_window.geometry("450x100")
        second_window.mainloop()
        
    def modify_contact_db(self, first_name, last_name, phone_number, email_address, old_contact, passed_window):
        """
        modify_contact_db

        This is the backend function to modify a contact

        First, check the email address to see if it is valid

        Then, set an error message if there is one

        if there is an error message
            -open a window
            -inform user of the error

        else
            -create the new contact
            -call the update_contact_db function
            -destroy the window containing the form
            -update the listbox
        """
        valid = None
        try:
            valid = validate_email(email_address)
        except:
            pass
            #I know except pass blocks are bad practice
            #I am handling the error in the elif block
            
        error_message = ""
        if self.validate_phone(phone_number) == False:
            error_message = "Phone Number is not in valid format"  
        elif not valid:
            error_message = "Email Address is not in valid format"

        if error_message != "":
            third_window = tk.Tk()
            third_window.title("Error!")
            third_window.configure(background="#5fb3b3")
            third_window_label = tk.Label(third_window, text=error_message)
            third_window_label.configure(background="#5fb3b3")
            third_window_label.config(font=("Arial", 24))
            third_window_label.pack()
            third_window.geometry("450x100")
        else:
            new_contact = contact.Contact(first_name.capitalize(), last_name.capitalize(), phone_number, email_address)
            update_contact_db(new_contact, old_contact)
            passed_window.destroy()
            self.update_list()

    def delete_contact(self, listbox_widget):
        """
        delete_contact

        This function is used to either confirm a deletion or rasie an error

        if the user has selected an option from the listbox
            -create a contact
            -call the delete_contact_db function and pass the newly created contact
            -create a window to let the user know that the contact is deleted
            -update the listbox
        
        else 
            -create a window to warn the user that no option was selected from the listbox
        """
        second_window = tk.Tk()
        index = listbox_widget.curselection()
        if index:
            contact = self.contacts_list[index[0]]
            delete_contact_db(contact)
            second_window.title(contact.get_first()+" "+contact.get_last())
            second_window.geometry("450x100")
            second_window.configure(background="#5fb3b3")
            label = tk.Label(second_window, text="You have deleted this contact!")
            label.config(font=("Arial", 24))
            label.configure(background="#5fb3b3")
            label.pack()
            self.update_list()
        else:
            second_window.title("Error!")
            second_window.configure(background="#5fb3b3")
            label = tk.Label(second_window, text="You must make a selection")
            label.config(font=("Arial", 24))
            label.configure(background="#5fb3b3")
            label.pack()
            second_window.geometry("450x100")
        second_window.mainloop()

    def validate_phone(self, phone_number):
        """
        validate_phone

        this method is used to validate if the phone number is a 10 character, numeric string
        """
        if phone_number.isnumeric() and len(phone_number)==10:
            return True
        return False

"""
if name is main
"""
if __name__ == "__main__":
    main_window = tk.Tk()
    app = ContactBuddy(main_window)
    main_window.mainloop()