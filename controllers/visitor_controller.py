
import mysql.connector
import mysql.connector.errors as err

# Cursor will come here ONLY IF try block is passed on without any exceptions.

def get_date(date):
	date_record = str(date).split("-")
	year = date_record[0]; month = date_record[1]; date_print = date_record[2]
	return [int(date_print), int(month), int(year)]

def add_visitor(connection:mysql.connector.connection.MySQLConnection, visitor_name, visitor_phone, visitor_email, visitor_address):
	visitor_name_data = list(visitor_name.split(" "))
	cursor = connection.cursor(buffered=True)

	visitor_f_name = visitor_name_data[0]
	if len(visitor_name_data) == 1:
		visitor_l_name = None
		visitor_name_data.remove(visitor_f_name)
		visitor_m_name = " ".join(visitor_name_data)
	elif len(visitor_name_data) == 2:
		visitor_l_name = visitor_name_data[1]
		visitor_name_data.remove(visitor_f_name)
		visitor_m_name = None
	else:
		visitor_l_name = visitor_name_data[-1]
		visitor_name_data.remove(visitor_f_name)
		visitor_name_data.remove(visitor_l_name)
		visitor_m_name = " ".join(visitor_name_data)

	sql = """
		INSERT INTO visitors 
			(visitor_fname, visitor_mname, visitor_lname, visitor_phone, visitor_email, visitor_address) 
		VALUES (%s, %s, %s, %s, %s, %s)
	"""
	values = (visitor_f_name, visitor_m_name, visitor_l_name, visitor_phone, visitor_email, visitor_address)

	cursor.execute(sql, values)
	connection.commit()
	print("Added user: ", end='')
	print([visitor_f_name, visitor_m_name, visitor_l_name, visitor_phone, visitor_email, visitor_address])


def edit_visitor(connection:mysql.connector.connection.MySQLConnection, visitor_id):
	field = ""
	cursor = connection.cursor(buffered=True)
	cursor.execute(f"   SELECT * FROM visitors WHERE visitor_uid = {visitor_id}   ")
	data = cursor.fetchone()
	fields = ["visitor_id", "visitor_fname", "visitor_mname", "visitor_lname", "visitor_phone", "visitor_email", "visitor_address", "visitor_date_of_join"]
	for i,j in zip(data, fields): print(j, "->", i)
	print("Select the field to be altered: ")
	print("1. First Name")
	print("2. Middle Name")
	print("3. Last Name")
	print("4. Phone Number")
	print("5. Email")
	print("6. Address")

	try:
		choice = str(input("Enter your choice: "))
		if choice == "1": field = "visitor_fname"
		elif choice == "2": field = "visitor_mname"
		elif choice == "3": field = "visitor_lname"
		elif choice == "4":	field = "visitor_phone"
		elif choice == "5":	field = "visitor_email"
		elif choice == "6":	field = "visitor_address"
	except TypeError: print("Input choice should be integer"); return;
	except ValueError: print("At least one selection has to be made"); return;
	except err.ConnectionTimeoutError or err.ProgrammingError: print("Might be something wring with database commands or values you passed for database analysis"); return;
	except err.DatabaseError: print("Error with database integrity"); return;

	new_value = str(input(f"Enter new value for '{field}' -> "))
	cursor.execute(f"   UPDATE visitors SET {field}='{new_value}' WHERE visitor_uid={visitor_id}   ")
	s = input(f"Set {field} to {new_value} for visitor with ID{visitor_id}? (y/n)")
	if s in "yY": print(f"Successfully changed '{field}' to '{new_value}' for user ID '{visitor_id}'"); connection.commit()
	else: print("Rolling back")

def find_visitor_information(connection:mysql.connector.connection.MySQLConnection):
	field = ""
	whatToSearch = str(input("Type in what you want to search: "))

	print("Select the field to be altered: ")
	print("1. First Name")
	print("2. Middle Name")
	print("3. Last Name")
	print("4. Phone Number")
	print("5. Email")
	print("6. Address")

	try:
		whereToSearch = str(input("Where to search the parameter for? "))
		if whereToSearch == "1": field = "visitor_fname"
		elif whereToSearch == "2": field = "visitor_mname"
		elif whereToSearch == "3": field = "visitor_lname"
		elif whereToSearch == "4": field = "visitor_phone"
		elif whereToSearch == "5": field = "visitor_email"
		elif whereToSearch == "6": field = "visitor_address"
	except TypeError: print("Input choice should be integer"); return;
	except ValueError: print("At least one selection has to be made"); return;
	except err.ConnectionTimeoutError or err.ProgrammingError: print("Might be something wring with database commands or values you passed for database analysis"); return;
	except err.DatabaseError: print("Error with database integrity"); return;

	cursor = connection.cursor(buffered=True)
	sql = f" SELECT * FROM visitors WHERE {field} LIKE '%{whatToSearch}%' "
	cursor.execute(sql)
	data = cursor.fetchall()

	if len(data) != 0:
		for i in data: print(i)
	else: print("No results found")

def view_visitor_details(connection: mysql.connector.connection.MySQLConnection):
	cursor = connection.cursor(buffered=True)
	sql = " SELECT * FROM visitors "
	cursor.execute(sql)
	data = cursor.fetchall()
	print("-" * 80)
	print(["VisitorID", "VisitorFName", "VisitorMName", "VisitorLName", "VisitorPhone", "VisitorEmail", "VisitorAddress", "VisitorDateOfJoin"])
	print("-" * 80)
	if len(data) != 0:
		for i in data: print(i)
	else: print("No results found")

# Will be modified when we create an 'issue controller'
def remove_visitor(connection: mysql.connector.connection.MySQLConnection, visitor_uid):
	cursor = connection.cursor(buffered=True)
	bookIssueCheck = f"  SELECT * FROM visitors WHERE visitor_uid = {visitor_uid}    "
	cursor.execute(bookIssueCheck)
	record = cursor.fetchone()
	booksIssuedToVisitor = record[8]
	if booksIssuedToVisitor == 0:
		sql = f"  DELETE FROM visitors WHERE visitor_uid = {visitor_uid};  "
		cursor.execute(sql)
		connection.commit()
	else:
		replyString = record[1] + " " + record[3] + " has " + str(booksIssuedToVisitor) + " books issued."
		print(replyString)
