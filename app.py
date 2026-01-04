from flask import Flask, render_template, request, redirect, url_for, flash, g
import mysql.connector
from db import get_db, close_db

app = Flask(__name__)
app.secret_key = 'dev_secret_key' # Change in production

app.teardown_appcontext(close_db)

@app.route('/')
def index():
    db = get_db()
    if db is None:
        return render_template('index.html', error="Database connection failed. Please check your credentials.")
    
    cursor = db.cursor(dictionary=True)
    
    # Dashboard Stats
    cursor.execute("SELECT COUNT(*) as count FROM books")
    total_books = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM visitors")
    total_visitors = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM book_issues WHERE issue_clear = 0")
    active_issues = cursor.fetchone()['count']
    
    cursor.close()
    
    return render_template('index.html', 
                           total_books=total_books, 
                           total_visitors=total_visitors, 
                           active_issues=active_issues)

# --- BOOKS ---
@app.route('/books')
def books():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    search = request.args.get('search')
    if search:
        query = "SELECT * FROM books WHERE book_name LIKE %s OR book_author LIKE %s"
        cursor.execute(query, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM books")
    
    books = cursor.fetchall()
    cursor.close()
    return render_template('books.html', books=books)

@app.route('/books/add', methods=['POST'])
def add_book():
    db = get_db()
    cursor = db.cursor()
    
    try:
        sql = """INSERT INTO books (book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity, book_current_quantity)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (
            request.form['book_name'],
            request.form['book_author'],
            request.form['book_genre'],
            request.form['book_publication_year'],
            request.form['book_issue_rate'],
            request.form['book_quantity'],
            request.form['book_quantity'] # Initial current quantity = total quantity
        )
        cursor.execute(sql, values)
        db.commit()
        flash('Book added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding book: {str(e)}', 'error')
    
    return redirect(url_for('books'))

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()
    # Check if safe to delete (all copies present) logic from CLI
    cursor.execute("SELECT book_quantity, book_current_quantity FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] == book[1]:
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        db.commit()
        flash('Book deleted successfully!', 'success')
    else:
        flash('Cannot delete book. Some copies are currently issued.', 'error')
        
    return redirect(url_for('books'))

# --- VISITORS ---
@app.route('/visitors')
def visitors():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    search = request.args.get('search')
    if search:
        query = "SELECT * FROM visitors WHERE visitor_fname LIKE %s OR visitor_lname LIKE %s OR visitor_phone LIKE %s"
        cursor.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM visitors")
        
    visitors = cursor.fetchall()
    cursor.close()
    return render_template('visitors.html', visitors=visitors)

@app.route('/visitors/add', methods=['POST'])
def add_visitor():
    db = get_db()
    cursor = db.cursor()
    
    full_name = request.form['name'].split()
    fname = full_name[0]
    lname = full_name[-1] if len(full_name) > 1 else ""
    mname = " ".join(full_name[1:-1]) if len(full_name) > 2 else ""
    
    try:
        sql = "INSERT INTO visitors (visitor_fname, visitor_mname, visitor_lname, visitor_phone, visitor_email, visitor_address) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (fname, mname, lname, request.form['phone'], request.form['email'], request.form['address'])
        cursor.execute(sql, values)
        db.commit()
        flash('Visitor added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding visitor: {str(e)}', 'error')
        
    return redirect(url_for('visitors'))

# --- ISSUES ---
@app.route('/issues')
def issues():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Get active issues
    cursor.execute("""
        SELECT i.issue_id, i.visitor_uid, i.book_id, i.return_date, v.visitor_fname, v.visitor_lname, b.book_name 
        FROM book_issues i
        JOIN visitors v ON i.visitor_uid = v.visitor_uid
        JOIN books b ON i.book_id = b.book_id
        WHERE i.issue_clear = 0
    """)
    issues = cursor.fetchall()
    
    cursor.close()
    return render_template('issues.html', issues=issues)

@app.route('/issues/create', methods=['POST'])
def create_issue():
    db = get_db()
    cursor = db.cursor(buffered=True) # buffered=True often helps with "Unread result found"
    
    book_id = request.form['book_id']
    visitor_id = request.form['visitor_id']
    return_date = request.form['return_date']
    
    try:
        # Calculate price (Logic from CLI: Rate * Days)
        cursor.execute(f"SELECT DATEDIFF('{return_date}', CURDATE())")
        days = cursor.fetchone()[0]
        
        cursor.execute("SELECT book_issue_rate FROM books WHERE book_id = %s", (book_id,))
        rate = cursor.fetchone()[0]
        
        price = rate * days
        
        # Insert Issue
        sql = "INSERT INTO book_issues (visitor_uid, book_id, return_date, book_issue_price) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (visitor_id, book_id, return_date, price))
        
        # Update Counts
        cursor.execute("UPDATE visitors SET books_issued = books_issued + 1 WHERE visitor_uid = %s", (visitor_id,))
        cursor.execute("UPDATE books SET book_current_quantity = book_current_quantity - 1 WHERE book_id = %s", (book_id,))
        
        db.commit()
        flash(f'Book issued! Price: {price}', 'success')
    except Exception as e:
        flash(f'Error issuing book: {str(e)}', 'error')
        
    return redirect(url_for('issues'))

@app.route('/issues/return/<int:issue_id>', methods=['POST'])
def return_book_route(issue_id):
    db = get_db()
    cursor = db.cursor(dictionary=True, buffered=True)
    
    try:
        cursor.execute("SELECT visitor_uid, book_id FROM book_issues WHERE issue_id = %s", (issue_id,))
        issue = cursor.fetchone()
        
        if issue:
            cursor.execute("UPDATE book_issues SET issue_clear = 1, return_date = CURDATE() WHERE issue_id = %s", (issue_id,))
            cursor.execute("UPDATE visitors SET books_issued = books_issued - 1 WHERE visitor_uid = %s", (issue['visitor_uid'],))
            cursor.execute("UPDATE books SET book_current_quantity = book_current_quantity + 1 WHERE book_id = %s", (issue['book_id'],))
            db.commit()
            flash('Book returned successfully!', 'success')
        else:
            flash('Issue record not found.', 'error')
    except Exception as e:
        flash(f'Error returning book: {str(e)}', 'error')
    
    return redirect(url_for('issues'))

if __name__ == '__main__':
    app.run(debug=True)
