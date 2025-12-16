
import mysql.connector
import mysql.connector.errors as err

def create_issue(connection: mysql.connector.connection.MySQLConnection, visitor, book_id, issue_date, return_date):
	cursor = connection.cursor(buffered = True)

	diff_query = f"   SELECT DATEDIFF('{return_date}', '{issue_date}');   "
	cursor.execute(diff_query)
	diff = cursor.fetchone()
	days_issued = diff[0]

	book_rate = f"  SELECT book_issue_rate FROM books WHERE book_id = {book_id};  "
	cursor.execute(book_rate)
	book_rate = cursor.fetchone()
	book_rate = book_rate[0]

	issue_name = f"  SELECT visitor_fname, visitor_lname FROM visitors WHERE visitor_uid = {visitor};  "
	cursor.execute(issue_name)
	issue_name = cursor.fetchone()
	issue_name = issue_name[0] + " " + issue_name[1]

	total_price = book_rate * days_issued
	print(total_price)

	sql = f"""
		INSERT INTO book_issues (visitor_uid, book_id, issue_date, return_date, book_issue_price)
		VALUES ({visitor}, {book_id}, '{issue_date}', '{return_date}', {total_price})
	"""

	# UPDATING OTHER FIELDS
	update_visitor = f"   UPDATE visitors SET books_issued = books_issued + 1 WHERE visitor_uid = {visitor};   "
	cursor.execute(update_visitor)

	update_book = f"   UPDATE books SET book_current_quantity = book_current_quantity - 1 WHERE book_id = {book_id};   "
	cursor.execute(update_book)

	cursor.execute(sql)
	x = input(f"CONFIRM -> Visitor ID: {visitor}, {issue_name} is issuing Book ID: {book_id} for {days_issued} days (y/n): ")
	if x in "yY": connection.commit()
	else: print("Rolling back")


def return_book(connection: mysql.connector.connection.MySQLConnection):
	cursor = connection.cursor(buffered = True)

	cursor.execute(f"   SELECT * FROM visitor_issue;   ")
	issue_record = cursor.fetchall()
	print(["IssueID", "IssueClear", "VisitorID", "VisitorName", "BookID", "BookName", "BookAuthor"])
	print("-"*80)
	for i in issue_record: print(i)
	print("-"*80)
	issue_id = int(input("Issue ID to be used: "))

	check_if_cleared = f"  SELECT * FROM book_issues WHERE issue_id = {issue_id};    "
	cursor.execute(check_if_cleared)
	record = cursor.fetchone()
	issue_cleared = record[6]
	visitor = record[2]
	book_id = record[1]

	if bool(issue_cleared):
		print("Issue ID is already cleared")
	else:
		update_issue = f"  UPDATE book_issues SET return_date = CURDATE() WHERE issue_id = {issue_id};  "
		update_issue_status = f"  UPDATE book_issues SET issue_clear = true WHERE issue_id = {issue_id};    "
		cursor.execute(update_issue)
		cursor.execute(update_issue_status)

		update_visitor = f"   UPDATE visitors SET books_issued = books_issued - 1 WHERE visitor_uid = {visitor};   "
		cursor.execute(update_visitor)

		update_book = f"   UPDATE books SET book_current_quantity = book_current_quantity + 1 WHERE book_id = {book_id};   "
		cursor.execute(update_book)

		x = input("CONFIRM -> Visitor ID: {visitor} is returning Book ID: {book_id} (y/n): ")
		if x in "yY": connection.commit()
		else: print("Rolling back")

# return_book - Add check for if the issue is cleared or not, if cleared, can not run again
# view - Visitor_id, visitor_name, issue_id, book_name

