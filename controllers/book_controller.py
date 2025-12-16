
import mysql.connector
import mysql.connector.errors as err

def add_book(connection:mysql.connector.connection.MySQLConnection,
		book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity):
	try:
		cursor = connection.cursor(buffered=True)
		sql = """
			INSERT INTO
				books ( book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity, book_current_quantity )
			VALUES 
				(%s, %s, %s, %s, %s, %s, %s);
		"""
		values = (book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity, book_quantity)
		cursor.execute(sql, values)
		connection.commit()

		print("Added book: ", end='')
		print([book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity])
	except err.ProgrammingError or err.ConnectionTimeoutError: print("Connection or syntax error"); return;
	except err.DatabaseError: print("Database Error"); return;

def edit_book(connection:mysql.connector.connection.MySQLConnection, book_id):
	field = ""
	cursor = connection.cursor(buffered=True)
	cursor.execute(f"   SELECT * FROM books WHERE book_id = {book_id}   ")
	data = cursor.fetchone()
	fields = ["book_id", "book_name", "book_author", "book_genre", "book_publication_year", "book_issue_rate", "book_quantity"]
	for i,j in zip(data, fields): print(j, "->", i)
	print("Select the field to be altered: ")
	print("1. Book Name")
	print("2. Book Author")
	print("3. Book Genre")
	print("4. Book Publication Year")
	print("5. Book Issue Rate")
	print("6. Book Quantity")

	try:
		choice = str(input("Enter your choice: "))
		if choice == "1": field = "book_name"
		elif choice == "2": field = "book_author"
		elif choice == "3": field = "book_genre"
		elif choice == "4": field = "book_publication_year"
		elif choice == "5": field = "book_issue_rate"
		elif choice == "6": field = "book_quantity"
	except TypeError: print("Input choice should be integer"); return;
	except ValueError: print("At least one selection has to be made"); return;
	except err.ConnectionTimeoutError or err.ProgrammingError: print("Might be something wring with database commands or values you passed for database analysis"); return;
	except err.DatabaseError: print("Error with database integrity"); return;

	if field in ["book_name", "book_author", "book_genre", "book_publication_year"]:
		new_value = str(input(f"Enter new value for {field}: "))
		cursor.execute(f"   UPDATE books SET {field} = '{new_value}' WHERE book_id = {book_id}   ")
	else:
		new_value = int(input(f"Enter new value for {field}: "))
		cursor.execute(f"   UPDATE books SET {field} = {new_value} WHERE book_id = {book_id}   ")

	s = input(f"Set {field} to {new_value} for book with ID{book_id}? (y/n)")
	if s in "yY": print(f"Successfully changed '{field}' to '{new_value}' for book ID '{book_id}'"); connection.commit()
	else: print("Rolling back")

def find_book_information(connection: mysql.connector.connection.MySQLConnection):
	field = ""
	whatToSearch = str(input("Type in what you want to search: "))

	print("Select the field to be altered: ")
	print("1. Book Name")
	print("2. Book Author")
	print("3. Book Genre")
	print("4. Book Publication Year")
	print("5. Book Issue Rate")
	print("6. Book Quantity")

	try:
		whereToSearch = str(input("Where to search the parameter for? "))
		if whereToSearch == "1": field = "book_name"
		elif whereToSearch == "2": field = "book_author"
		elif whereToSearch == "3": field = "book_genre"
		elif whereToSearch == "4": field = "book_publication_year"
		elif whereToSearch == "5": field = "book_issue_rate"
		elif whereToSearch == "6": field = "book_quantity"
	except TypeError: print("Input choice should be integer"); return;
	except ValueError: print("At least one selection has to be made"); return;
	except err.ConnectionTimeoutError or err.ProgrammingError: print("Might be something wring with database commands or values you passed for database analysis"); return;
	except err.DatabaseError: print("Error with database integrity"); return;

	cursor = connection.cursor(buffered=True)
	sql = f" SELECT * FROM books WHERE {field} LIKE '%{whatToSearch}%' "
	cursor.execute(sql)
	data = cursor.fetchall()

	if len(data) != 0:
		for i in data: print(i)
	else: print("No results found")

def view_book_details(connection: mysql.connector.connection.MySQLConnection):
	cursor = connection.cursor(buffered=True)
	sql = "  SELECT * FROM books  "
	cursor.execute(sql)
	book_record = cursor.fetchall()
	if len(book_record) == 0: print("-"*80); print("No records found")
	else:
		print("-"*38 + "BOOK" + "-"*38)
		print("-"*80)
		print(["BookID", "BookName", "BookAuthor", "BookGenre", "BookPublicationYear", "BookQuantity", "BookCurrentQuantity"])
		print("-"*80)
		for i in book_record: print(i)

def update_book_availability(connection:mysql.connector.connection.MySQLConnection, book_id):
	sql = f"   SELECT * FROM books WHERE book_id = {book_id};   "
	cursor = connection.cursor(buffered=True)
	cursor.execute(sql)
	record = cursor.fetchone()
	try: new_book_availability = int(input("Enter new book quantity: "))
	except ValueError: print("Value must be integer, back to menu and try again"); return
	sql = f"   UPDATE books SET book_current_quantity = {new_book_availability} WHERE book_id = {book_id};   "
	cursor.execute(sql)
	confirm = input(f"CONFIRM -> Updating Book ID {book_id} titled {record[1]}'s quantity update to {new_book_availability} (y/n): ")
	if confirm in "yY": connection.commit();
	else: print("Rolling back")

def remove_book_from_library_inventory(connection: mysql.connector.connection.MySQLConnection, book_id):
	cursor = connection.cursor(buffered=True)
	sql = f"   SELECT * FROM books WHERE book_id = {book_id};   "
	cursor.execute(sql)
	record = cursor.fetchone()
	current_books = record[7]
	assumed_record = record[6]
	if current_books == assumed_record:
		delete = f"   DELETE FROM books WHERE book_id = {book_id};   "
		cursor.execute(delete)
		x = str(input(f"CONFIRM -> Removing book ID {record[0]} titled {record[1]} (y/n): "))
		if x in "yY": connection.commit()
		else: print("Rolling back")
	else: print(f"Currently all copies are not present\nCurrent: {current_books}\nAssumed: {assumed_record}\nCollect these books before removing them from the library")
