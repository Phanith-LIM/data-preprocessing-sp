import os
from natsort import natsorted

def read_files(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r') as f:  # Fallback encoding
            return f.read()

def process_content(content):
    symbols_to_remove = [
        '(', ')', '[', ']', '{', '}', '<', '>', 
        '“', '”', '‘', '’', '«', '»', ',',
        '「', '」', '『', '』', '▁', '-',
        '៖', '។', '៛', '៕', '!', '​', '–'
    ]
    for symbol in symbols_to_remove:
        content = content.replace(symbol, '')
    content = content.replace('៛', 'រៀល')
    content = content.replace('.', 'ចុច')
    content = ''.join(char.lower() if 'A' <= char <= 'Z' else char for char in content)
    return content

def process_files_in_directory(directory_path):
    files = os.listdir(directory_path)
    files = [f for f in files if f.endswith('.txt')]
    files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
    files = natsorted(files)

    for file in files:
        file_path = os.path.join(directory_path, file)
        content = read_files(file_path)
        processed_content = process_content(content)
        with open(file_path, 'w') as f:
            f.write(processed_content)
        print(f"✅ {file} processed successfully!")

# path = '/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean/4'
# if os.path.exists(path):
#     process_files_in_directory(path)
#     print("All files processed successfully!")
# else:
#     print(f"Error: Directory '{path}' does not exist.")
