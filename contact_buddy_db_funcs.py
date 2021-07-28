#import contact module
import Contact.contact as contact
import sqlite3

"""
connect to the database
"""
DB_FILENAME = 'contacts.db'

conn = sqlite3.connect(DB_FILENAME)

def save_contact_db(new_contact):
	"""
	Save Contact to the database

	If the passed paramenter is a Contact object, then insert it into the database

	Else rasie a type error
		-this will be rare, as it is difficult to pass anything other than a Contact object to this method
	"""
	if isinstance(new_contact, contact.Contact):
		conn.execute(f"INSERT INTO contacts (first_name, last_name, phone_number, email_address) VALUES ('%s', '%s', '%s', '%s')" % (new_contact.get_first(), new_contact.get_last(), new_contact.get_phone(), new_contact.get_email()))
		conn.commit()
		pass
	else:
		raise TypeError("Parameter passed was not a Contact")

def update_contact_db(updated_contact, old_contact):
	"""
	Update Contact in the database

	If both of the passed paramenters are Contact objects, then update the old information to the new information in the database

	Else rasie a type error
		-this will be rare, as it is difficult to pass anything other than a Contact object to this method
	"""
	if isinstance(updated_contact, contact.Contact) and isinstance(old_contact, contact.Contact):
		conn.execute(f"UPDATE contacts SET first_name='%s', last_name='%s', phone_number='%s', email_address='%s' WHERE first_name='%s' AND last_name='%s' AND phone_number='%s' AND email_address='%s'" % (updated_contact.get_first(), updated_contact.get_last(), updated_contact.get_phone(), updated_contact.get_email(), old_contact.get_first(), old_contact.get_last(), old_contact.get_phone(), old_contact.get_email()))
		conn.commit()
	else:
		raise TypeError("Parameter passed was not a Contact")

def delete_contact_db(contact_to_delete):
	"""
	Delete Contact from the database 

	If the passed paramenter is a Contact object, then delete it from the database

	Else rasie a type error
		-this will be rare, as it is difficult to pass anything other than a Contact object to this method
	"""
	if isinstance(contact_to_delete, contact.Contact):
		conn.execute(f"DELETE FROM contacts WHERE first_name='%s' AND last_name='%s' AND phone_number='%s' AND email_address='%s'" % (contact_to_delete.get_first(), contact_to_delete.get_last(), contact_to_delete.get_phone(), contact_to_delete.get_email()))
		conn.commit()
	else:
		raise TypeError("Parameter passed was not a Contact")