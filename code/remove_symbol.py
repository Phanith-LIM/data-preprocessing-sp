import os
from natsort import natsorted

def read_files(path):
    with open(path, 'r', encoding='utf-8') as f:  # Ensure encoding supports special characters
        return f.read()  # Read entire file as a single string

path = r'sample'
files = os.listdir(path)
files = [f for f in files if os.path.isfile(os.path.join(path, f))]
files = natsorted(files)

for file in files:
    file_path = os.path.join(path, file)
    content = read_files(file_path)

    # Remove symbols from the content
    content = content.replace('(', '').replace(')', '')
    content = content.replace('[', '').replace(']', '')
    content = content.replace('{', '').replace('}', '')
    content = content.replace('<', '').replace('>', '')
    content = content.replace('“', '').replace('”', '')
    content = content.replace('‘', '').replace('’', '')
    content = content.replace('«', '').replace('»', '')
    content = content.replace('「', '').replace('」', '')
    content = content.replace('『', '').replace('』', '')
    content = content.replace('▁', '')
    # Write the modified content back to the file
    print(f"✅ {file} processed successfully!")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Parentheses removed successfully!")
