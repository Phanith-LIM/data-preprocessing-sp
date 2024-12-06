import re
import os
from natsort import natsorted
from tha.decimals import processor
from helper.io import get_first_line, remove_first_line, read_text_file, write_text_file
from helper.remove_symbol import process_content
import pandas as pd

def replace_khmer_numbers(content, pattern):
    def convert_number(match):
        khmer_number = match.group(0)
        return processor(khmer_number)
    return re.sub(pattern, convert_number, content)

def process_file(folder_name: str, khmer_number_pattern: str):
    content = read_text_file(folder_name)
    content = process_content(content)
    content = replace_khmer_numbers(content, khmer_number_pattern)
    content = content.replace('▁', '')
    write_text_file(folder_name, content)

def process_log_file(log_file: str, output_path: str):
    df = pd.read_csv(log_file)
    df['speaker'] = [None] * len(df)
    csv_files = os.listdir(path)
    csv_files = [f for f in csv_files if f.endswith('txt')]
    csv_files = natsorted(csv_files)

    for file in csv_files:
        file_path = os.path.join(path, file)
        speakers = get_first_line(file_path)
        speakers = speakers.replace('\n', '')
        speakers = speakers.replace('​', '')
        file_id = int(file.split('.')[0])
        df.loc[df['id'] == file_id, 'speaker'] = speakers
        remove_first_line(file_path)

        column_order = list(df.columns)
        author_index = column_order.index('author')
        column_order.insert(author_index + 1, column_order.pop(column_order.index('speaker')))
        df = df[column_order]
        df.to_csv(output_path, index=False)

if __name__ == '__main__':
    number_page = 4
    path = f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean/{number_page}'
    log_path = f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/logs/{number_page}.csv'
    output_path = f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean-logs/{number_page}.csv'

    khmer_num_pattern = r'[០-៩]+'
    files = [os.path.join(path, f) for f in natsorted(os.listdir(path)) if f.endswith('.txt')]
    for file in files:
        process_file(folder_name=file, khmer_number_pattern=khmer_num_pattern)
    process_log_file(log_file=log_path, output_path=output_path)
    print('Done')