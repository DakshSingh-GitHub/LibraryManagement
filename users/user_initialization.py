import pickle
import os

def initialize_file(first_user):
    users = [first_user]
    file_path = os.path.join(os.path.dirname(__file__), 'users.bin')
    
    with open(file_path, 'wb') as f:
        pickle.dump(users, f)
    
    print(f"Initialized {file_path} with first user.")
