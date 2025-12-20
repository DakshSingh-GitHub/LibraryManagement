import mysql.connector as mysql
import mysql.connector.errors as err
import os

# noinspection PyUnusedImports
import controllers.visitor_controller.visitor_controller as visitors
# noinspection PyUnusedImports
import controllers.reception_controller.issue_controller as issues
# noinspection PyUnusedImports
import controllers.admin_controller.admin_controller as users

try: lib = mysql.connect(host="127.0.0.1", username="root", password="root", database="library"); cursor = lib.cursor(buffered=True)
except err.ProgrammingError as e: print("Incorrect username/password") ; os._exit(0)
except err.ConnectionTimeoutError as e: print("Timeout Connection"); os._exit(0)

# noinspection PyBroadException
try:
	# cursor.execute("SELECT * FROM book_issues where issue_id = 4;")
	# record = cursor.fetchone()
	# print(bool(record[6]))
	issues.return_book(lib)
except Exception as e:
	print("Might be wrong book ID")

issues.return_book(lib)
