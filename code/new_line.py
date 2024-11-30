import os
from natsort import natsorted

def read_files(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read() 
path = r'sample'
files = os.listdir(path)
files = [f for f in files if os.path.isfile(os.path.join(path, f))]
files = natsorted(files)

for file in files:
    file_path = os.path.join(path, file)
    content = read_files(file_path)
    content = content.replace('។', '\n').replace('៕', '\n')
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    new_content = '\n'.join(lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Files processed successfully!")
