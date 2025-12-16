
import os
import mysql.connector as mysql
import mysql.connector.errors as err

import controllers.visitor_controller as visitors
import controllers.book_controller as books

try: lib = mysql.connect(host="127.0.0.1", username="root", password="root", database="library"); cursor = lib.cursor(buffered=True)
except err.ProgrammingError as e: print("Incorrect username/password") ; os._exit(0)
except err.ConnectionTimeoutError as e: print("Timeout Connection"); os._exit(0)

while True:
	try:
		os.system("cls")
		print("---------------------GREAT LIBRARY (Press n+enter to exit)----------------------")
		print("n + enter -> Exit the terminal prompt")
		print("ctrl + c -> on any screen, takes you back to the main menu")
		print("--------------------------------VISITORS----------------------------------------")
		print("V1. Add Visitor, Welcome newcomer")
		print("V2. Edit User, got some new updates about ya?")
		print("V3. See all visitor information")
		print("V4. Find visitor information (by any parameter)")
		print("----------------------------------BOOKS-----------------------------------------")
		print("B1. Add New Book, New Arrivals :)")
		print("B2. Edit Books, change records of books")
		print("B3. See all book information")
		print("B4. Find book by information and field")
		print("B5. Update the current availability of a book")
		print("B6. Remove Book from library")
		print("-----------------------------------ISSUES---------------------------------------")
		print("I1. Issue a book to visitor")
		print("--------------------------------Bye Bye-----------------------------------------")
		print("n. Exit")
		print("-" * 80)

		choice = str(input("Enter your choice: "))

		if choice in ["V1", 'v1']:
			name = str(input("Enter Visitor's good name: "))
			phone = str(input("Enter Visitor's phone number: "))
			email = str(input("Enter Visitor's email: "))
			address = str(input("Enter Visitor's address: "))
			visitors.add_visitor(lib, name, phone, email, address)
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")

		elif choice in ["V2", "v2"]:
			# noinspection PyBroadException
			try:
				visitor_id = int(input("Enter Visitor's ID: "))
				visitors.edit_visitor(lib, visitor_id)
			except Exception:
				ch = str(input("Might be mistake in ID provided. Want to find ID?"))
				if ch in "yY": visitors.find_visitor_information(lib)
				print("Hope you found the visitor :).....Sorry for the inconvenience, but please start from the menu again")
			print("-"*80)
			input("press any key to continue")
			os.system("cls")

		elif choice in ["V3", "v3"]:
			visitors.view_visitor_details(lib)
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")

		elif  choice in ["V4", "v4"]:
			visitors.find_visitor_information(lib)
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")

		elif choice in ["B1", "b1"]:
			book_name = str(input("Enter book name: "))
			book_author = str(input("Enter book author: "))
			book_genre = str(input("Enter book genre: "))
			book_publication_year = int(input("Enter book publication year: "))
			book_issue_rate = int(input("Enter book Issue rate: "))
			book_quantity = int(input("Enter book quantity: "))
			books.add_book(lib, book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity)
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")

		elif choice in ["B2", "b2"]:
			book_id = int(input("Enter book ID: "))
			books.edit_book(lib, book_id)
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")

		elif choice in ["B3", "b3"]:
			books.view_book_details(lib)
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")

		elif choice in ["B4", "b4"]:
			books.find_book_information(lib)
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")

		elif choice in ["B5", "b5"]:
			try:
				book_id = int(input("Enter Book ID: " ))
				books.update_book_availability(lib, book_id)
			except ValueError as e: print("Wrong input type")
			finally:
				print("-" * 80)
				input("press any key to continue")
				os.system("cls")

		elif choice in ["B6", "b6"]:
			try:
				book_id = int(input("Enter Book ID: " ))
				books.remove_book_from_library_inventory(lib, book_id)
			except ValueError as e: print("Wrong input type")
			finally:
				print("-" * 80)
				input("press any key to continue")
				os.system("cls")

		elif choice == "n": break
		else:
			print("Invalid console choice")
			print("-" * 80)
			input("press any key to continue")
			os.system("cls")
	except KeyboardInterrupt: print()

os.system("cls")