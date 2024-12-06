import os
from natsort import natsorted
import pandas as pd
from helper.io import get_first_line, remove_first_line

number_page = 4
path = f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean/{number_page}'
path_csv = f'/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/clean-logs/{number_page}.csv'

df = pd.read_csv(path_csv)
df['speaker'] = [None] * len(df)

files = os.listdir(path)
files = [file for file in files if file.endswith('txt')]
files = natsorted(files)


for file in files:
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
    df.to_csv(path_csv, index=False)
    print(f"{file} -> {file_id}, speaker: {speakers}")

print("Done!")