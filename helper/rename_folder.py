import os
import string
from prettytable import PrettyTable

# Define parameters in a dictionary
number = 69
para = {
    'root_folder': f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/clean/WMC-clean/WMC-short/{number}',
    'start_from': 38
}

# Extract parameters
root_folder = para['root_folder']
start_from = para['start_from']

# Get all folders and sort them alphabetically
folders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
folders = sorted(folders)
folder_mapping = {old_name: letter for old_name, letter in zip(folders, string.ascii_lowercase)}


table = PrettyTable()
table.field_names = ["Folder", "Renamed"]

# Step 1: Rename folders to temporary names (letters)
for old_name, letter in folder_mapping.items():
    old_path = os.path.join(root_folder, old_name)
    new_path = os.path.join(root_folder, letter)
    os.rename(old_path, new_path)

# Step 2: Rename folders to the final numbered names
current_number = start_from
for old_name, letter in folder_mapping.items():
    old_folder_path = os.path.join(root_folder, letter)
    new_folder_name = str(current_number)
    new_folder_path = os.path.join(root_folder, new_folder_name)
    os.rename(old_folder_path, new_folder_path)

    # Add the renaming details to the PrettyTable
    table.add_row([old_name, new_folder_name])
    current_number += 1

# Print the summary using PrettyTable
print("\nSummary of Folder Renaming:")
print(table)
print("\n✅ - All folders have been renamed successfully.")
