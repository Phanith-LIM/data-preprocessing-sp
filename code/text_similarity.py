import difflib
import os
import pandas as pd
from natsort import natsorted
from prettytable import PrettyTable

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
def calculate_similarity(text1, text2):
    sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
    return sequence_matcher.ratio() * 100  

text = read_file('sample/3.txt')

path = r'/Users/PhanithLIM/Documents/05. Dataset/Speech Recognition/processing/ទស្សនៈព្រឹត្តិការណ៍ពិភពលោក'
folders = os.listdir(path)
folders = [f for f in folders if os.path.isdir(os.path.join(path, f))]
folders = natsorted(folders)
info_list = []

# Loop through each folder and file
for folder in folders:
    files = os.listdir(os.path.join(path, folder))
    files = [f for f in files if f.endswith('.txt')]
    files = natsorted(files)
    
    for file in files:
        text2 = read_file(os.path.join(path, folder, file))
        similarity = calculate_similarity(text, text2)
        info_list.append({
            'folder': folder,
            'file': file,
            'similarity': similarity
        })
    
    print(f'✅ - {folder} comparison done.')
df = pd.DataFrame(info_list)
df = df.sort_values('similarity', ascending=False)
df = df[df['similarity'] > 40]
df.to_csv('output/output.csv', index=False)
print('✅ - Done.')
print('👉 - Check the output folder for the result.')


# Pretty print the result
table = PrettyTable()
table.field_names = ["Folder", "File", "Similarity (%)"]
for index, row in df.iterrows():
    table.add_row([row['folder'], row['file'], f"{row['similarity']:.2f}"])
print(table)
