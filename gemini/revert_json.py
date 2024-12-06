import json
import os
from natsort import natsorted

def read_json(path: str):
    with open(path, 'r') as f:
        d = json.load(f)
    return d

page_number = 2
path = f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean/{page_number}'

target_path = 'meta/output.json'
original_path = 'meta/original.json'

target = read_json(target_path)
original = read_json(original_path)

files = os.listdir(path)
files = [file.replace('.txt', '') for file in files if file.endswith('.txt')]
files = natsorted(files)

meta_data = {}
for file in files:
    words = original[file]

    body = {
        word: target.get(word, None) for word in words
    }
    meta_data[file] = body

with open(f'output/{page_number}.json', 'w') as f:
    json.dump(meta_data, f, indent=4, ensure_ascii=False)
print("Reverse json done!.")
