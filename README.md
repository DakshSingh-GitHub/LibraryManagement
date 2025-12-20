# Library Management System

A command-line based Library Management System written in Python. This system allows for the management of books, visitors, and book issuance. It uses a MySQL database to store and retrieve data.

## Features

*   **Book Management:**
    *   Add new books to the library inventory.
    *   Edit existing book details.
    *   Search for books by name, author, genre, etc.
    *   View a list of all books in the library.
    *   Update the availability of books.
    *   Remove books from the inventory.
*   **Visitor Management:**
    *   Register new visitors.
    *   Edit visitor information.
    *   Search for visitors.
    *   View a list of all registered visitors.
    *   Remove visitors from the system.
*   **Book Issuance:**
    *   Issue books to visitors.
    *   Record the issue date and calculate the return date and price.
    *   Return books and update their availability.
    *   View the history of book issues.
*   **User Management (Admin):**
    *   Add new system users (admins, staff, etc.).
    *   View all system users.
    *   Delete system users.
    *   Check user roles.

## Setup

1.  **Prerequisites:**
    *   Python 3
    *   MySQL Server
    *   `mysql-connector-python` library (`pip install mysql-connector-python`)

2.  **Database Setup:**
    *   Create a MySQL database named `library`.
    *   Execute the SQL script in `queries/lib.sql` to create the necessary tables and views.

3.  **Configuration:**
    *   Update the database connection details in `main.py` if they are different from the default (host=`127.0.0.1`, user=`root`, password=`root`).

4.  **Running the Application:**
    *   Run `main.py` from your terminal:
        ```bash
        python main.py
        ```

## Database Schema

The database consists of three main tables:

*   `books`: Stores information about the books.
*   `visitors`: Stores information about the library visitors.
*   `book_issues`: Stores information about book issuance.

A view named `visitor_issue` is also created to provide a consolidated view of issue details.

## Application Usage

The application provides a command-line menu to interact with the different management functions.

## Controllers

The application's logic is separated into several controllers organized by function:

*   **`controllers/admin_controller/`**
    *   `admin_controller.py`: Manages system users and their roles.
*   **`controllers/reception_controller/`**
    *   `book_controller.py`: Contains all functions related to book management.
    *   `issue_controller.py`: Contains all functions related to book issuance and returns.
*   **`controllers/visitor_controller/`**
    *   `visitor_controller.py`: Contains all functions related to visitor management.

---

## Controller Methods

### `controllers/admin_controller/admin_controller.py`

*   **`add_users(username)`**
    *   Adds a new user to the system. It checks if the username already exists. If not, it prompts for the user's name, password, role, and a note, then adds the user to the `users` list.
*   **`view_users()`**
    *   Iterates through the `users` list and prints the username, name, and role of each user.
*   **`delete_user(username)`**
    *   Removes a user from the `users` list based on the provided `username`. It prints a success message if found, or a "not found" message otherwise.
*   **`check_if_user(username)`**
    *   Checks if a user with the given `username` exists in the system. Returns `True` if found, `False` otherwise.
*   **`check_role(username)`**
    *   Retrieves the role of a specific user identified by `username`. Returns the role string if found, or `None` if the user does not exist.

### `controllers/reception_controller/book_controller.py`

*   **`add_book(connection, book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity)`**
    *   Adds a new book to the `books` table with the provided details.
*   **`edit_book(connection, book_id)`**
    *   Allows editing the details of an existing book identified by `book_id`. It prompts the user to select a field to modify and then updates the record.
*   **`find_book_information(connection)`**
    *   Searches for books in the database based on user-provided criteria (e.g., name, author).
*   **`view_book_details(connection)`**
    *   Displays a formatted list of all books currently in the `books` table.
*   **`update_book_availability(connection, book_id)`**
    *   Updates the `book_current_quantity` for a specific book, which is useful when a book is returned or lost.
*   **`remove_book_from_library_inventory(connection, book_id)`**
    *   Deletes a book from the `books` table. It includes a check to prevent deletion if not all copies of the book are currently in the library.

### `controllers/reception_controller/issue_controller.py`

*   **`create_issue(connection, visitor, book_id, return_date)`**
    *   Creates a new book issue record. It calculates the total price based on the book's rate and the duration of the issue. It also updates the `books_issued` count for the visitor and decrements the `book_current_quantity` for the book.
*   **`return_book(connection)`**
    *   Handles the process of a book being returned. It marks the issue as cleared, sets the return date to the current date, and updates the corresponding visitor and book records.

### `controllers/visitor_controller/visitor_controller.py`

*   **`add_visitor(connection, visitor_name, visitor_phone, visitor_email, visitor_address)`**
    *   Adds a new visitor to the `visitors` table. It parses the full name into first, middle, and last names.
*   **`edit_visitor(connection, visitor_id)`**
    *   Allows editing the details of an existing visitor identified by `visitor_id`.
*   **`find_visitor_information(connection)`**
    *   Searches for visitors based on user-inputted search terms and fields.
*   **`view_visitor_details(connection)`**
    *   Displays a formatted list of all registered visitors.
*   **`remove_visitor(connection, visitor_uid)`**
    *   Removes a visitor from the `visitors` table, but only if they have no books currently issued to them.
