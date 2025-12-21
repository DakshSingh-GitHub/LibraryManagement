import pickle
import os

# Path to the users.bin file
# Assuming the structure is:
# Project/
#   controllers/
#     admin_controller/
#       admin_controller.py
#   users/
#     users.bin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USERS_FILE = os.path.join(BASE_DIR, 'users', 'users.bin')

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, 'rb') as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        return []

def save_users(users_data):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'wb') as f:
        pickle.dump(users_data, f)

def add_users(username):
    users = load_users()
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
        save_users(users)
        print(f"User '{username}' added successfully.")
    else:
        print(f"User '{username}' already exists")

def view_users():
    users = load_users()
    if not users:
        print("No users found.")
    for user in users:
        print(f"Username: {user['username']}\nName: {user['name']}\nRole: {user['role']}")
        print("-" * 20)

def delete_user(username):
    users = load_users()
    user_to_remove = None
    for user in users:
        if user["username"] == username:
            user_to_remove = user
            break
    
    if user_to_remove:
        users.remove(user_to_remove)
        save_users(users)
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found.")

def check_if_user(username):
    users = load_users()
    existing_usernames = [user["username"] for user in users]

    if username not in set(existing_usernames):
        return False
    else:
        return True

def check_role(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user["role"]
    return None
