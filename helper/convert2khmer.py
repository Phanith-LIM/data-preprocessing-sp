import re
import os
from natsort import natsorted
from tha.decimals import processor

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def write_text_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)

path = '/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean/4'
khmer_number_pattern = r'[០-៩]+'
files = [f for f in os.listdir(path) if f.endswith('.txt')]
files = natsorted(files)

def replace_khmer_number(match):
    khmer_number = match.group(0)
    return processor(khmer_number)

for file in files:
    file_path = os.path.join(path, file)
    text = read_text_file(file_path)
    text = re.sub(khmer_number_pattern, replace_khmer_number, text)
    text = text.replace('%', 'ភាគរយ')
    text = text.replace('▁', '')
    write_text_file(file_path, text)
    print(f"Processed {file}")
