import pickle
import os

users = []
file_path = os.path.join(os.path.dirname(__file__), 'users.bin')

with open(file_path, 'wb') as f:
    pickle.dump(users, f)

print(f"Initialized {file_path}")
