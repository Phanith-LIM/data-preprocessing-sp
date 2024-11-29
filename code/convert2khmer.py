import tha
import re
import tha.decimals
import os

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def extract_khmer_numbers_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    pattern = r'[០-៩]+'
    khmer_numbers = re.findall(pattern, text)
    return khmer_numbers
    
path = 'sample'
folder = os.listdir(path)
for file in folder:
    numbers = extract_khmer_numbers_from_file(f'{path}/{file}')
    texts = read_file(f'{path}/{file}')
    for number in numbers:
        texts = texts.replace(number, tha.decimals.processor(number))
    with open(f'{path}/{file}', 'w', encoding='utf-8') as f: