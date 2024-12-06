import os
from natsort import natsorted
import re
import json

def extract_words_from_files(path):
    def read_text_file(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    pattern = r'\b[a-zA-Z]+\b'
    files = os.listdir(path)
    files = [file for file in files if file.endswith('.txt')]
    files = natsorted(files)
    body = {}  # Dictionary to store results
    for file in files:
        file_path = os.path.join(path, file)
        text = read_text_file(file_path)
        words = re.findall(pattern, text)
        body[file.replace('.txt', '')] = words
    with open('meta/original.json', 'w') as f:
        json.dump(body, f, indent=4)
    return json.dumps(body, indent=4)

# Example usage
# path = '/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean/1'
# result_json = extract_words_from_files(path)
#
# with open('meta/original.json', 'w') as f:
#     f.write(result_json)
