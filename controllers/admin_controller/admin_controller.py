
from users.users import users

def add_users(username):
	existing_usernames = []
	for user in users:
		existing_usernames.append(user["username"])
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
	else:
		print(f"User '{username}' already exists")

def view_users():
	for user in users: print(f"Username: {user['username']}\nName: {user['name']}\nRole: {user['role']}")

def delete_user(username):
	for user in users:
		if user["username"] == username:
			print(f"User '{username}' deleted successfully.")
			users.remove(user)
	else:
		print(f"User '{username}' not found.")

def check_if_user(username):
	existing_usernames = []
	for user in users:
		existing_usernames.append(user["username"])

	if username not in set(existing_usernames): return False
	else: return True

def check_role(username):
	# checks the role of user
	for user in users:
		if user["username"] == username:
			return user["role"]
			break
	return None
