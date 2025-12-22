import pickle
import os

# Path to the users.bin file
# Assuming the structure is:
# Project/
#   controllers/
#     admin_controller/
#       admin_controller.py
#   dataset/
#     users.bin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USERS_FILE = os.path.join(BASE_DIR, 'dataset', 'users.bin')

# Define the public interface of this module
__all__ = ['add_users', 'view_users', 'delete_user', 'check_if_user', 'check_role', 'edit_user']

def _load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, 'rb') as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        return []

def _save_users(users_data):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'wb') as f:
        pickle.dump(users_data, f)

def add_users(username):
    users = _load_users()
    existing_usernames = [user["username"] for user in users]
    
    if username not in set(existing_usernames):
        name = str(input("Enter name: "))
        password = str(input("Enter password: "))
        role = str(input("Enter role: "))
        note = str(input("Enter note: "))
        new_user = {
            "username": username.lower(),
            "name": name,
            "password": password,
            "role": role,
            "note": note
        }
        users.append(new_user)
        _save_users(users)
        print(f"User '{username}' added successfully.")
    else:
        print(f"User '{username}' already exists")

def view_users():
    users = _load_users()
    if not users:
        print("No users found.")
    for user in users:
        print(f"Username: {user['username']}\nName: {user['name']}\nRole: {user['role']}\nNote:{user['note']}")
        print("-" * 20)

def delete_user(username):
    users = _load_users()
    user_to_remove = None
    for user in users:
        if user["username"] == username:
            user_to_remove = user
            break
    
    if user_to_remove:
        users.remove(user_to_remove)
        _save_users(users)
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found.")

def check_if_user(username):
    users = _load_users()
    existing_usernames = [user["username"] for user in users]

    if username not in set(existing_usernames):
        return False
    else:
        return True

def check_role(username):
    users = _load_users()
    for user in users:
        if user["username"] == username:
            return user["role"]
    return None

def edit_user(username_to_edit):
    username_to_edit = username_to_edit.lower()
    users = _load_users()
    user_found = False
    for user in users:
        if user["username"] == username_to_edit:
            user_found = True
            print(f"Editing user: {user['username']}")
            print("Leave field blank to keep current value.")

            new_name = str(input(f"Enter new name (current: {user['name']}): "))
            if new_name: user['name'] = new_name
            new_password = str(input(f"Enter new password (current: {'*' * len(user['password'])}): "))
            if new_password: user['password'] = new_password
            new_role = str(input(f"Enter new role (current: {user['role']}): "))
            if new_role: user['role'] = new_role
            new_note = str(input(f"Enter new note (current: {user['note']}): "))
            if new_note: user['note'] = new_note

            _save_users(users)
            print(f"User '{username_to_edit}' updated successfully.")
            break
    if not user_found:
        print(f"User '{username_to_edit}' not found.")
