class Contact:
	"""
	Contact Class

	This object holds the information a contact would have
		- First Name
		- Last Name
		- Phone Number
		- Email Address
	It will be used throughout the application

	It only needs getter functions
	"""

	def __init__(self, first_name, last_name, phone_number, email_address):
		"""
		Constructor
		
		This will be used to initialize contacts
		"""
		self.first_name = first_name
		self.last_name = last_name
		self.phone_number = phone_number
		self.email_address = email_address
			
	"""
	Getter functions for all variables
	"""
	def get_first(self):
		return self.first_name
	
	def get_last(self):
		return self.last_name
		  
	def get_phone(self):
		return self.phone_number
		
	def get_email(self):
		return self.email_address
		
# 	"""
# 	Str function to test Contact class
# 	"""
# 	def __str__(self):
# 		return f"{self.first_name} {self.last_name}\n{self.phone_number}\n{self.email_address}"
		

# """

# """
# if __name__ == "__main__":
# 	c = Contact("John", "Smith", "5045550987", "jsmith@gmail.com")
# 	print(c)