import PyInstaller.__main__
import os

# Define the path to the dataset folder
dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')

# Define the separator for add-data (semicolon for Windows, colon for Unix)
separator = ';' if os.name == 'nt' else ':'

# Construct the add-data argument
add_data_arg = f'{dataset_path}{separator}dataset'

print("Building executable...")
print(f"Adding data from: {add_data_arg}")

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--name=LibraryManagement',
    f'--add-data={add_data_arg}',
    '--clean',
    # '--windowed', # Uncomment if you don't want a console window
])

print("Build complete. Check the 'dist' folder.")
