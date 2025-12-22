import pickle
import os

def initialize_file(first_user):
    users = [first_user]
    # Go up one level from 'users' directory, then into 'dataset'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(base_dir, 'dataset')
    file_path = os.path.join(dataset_dir, 'users.bin')
    
    os.makedirs(dataset_dir, exist_ok=True)
    
    with open(file_path, 'wb') as f:
        pickle.dump(users, f)
    
    print(f"Initialized {file_path} with first user.")
