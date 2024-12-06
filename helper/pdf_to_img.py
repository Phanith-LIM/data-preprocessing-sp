import os
from natsort import natsorted
from pdf2image import convert_from_path

input_folder = r'/Users/PhanithLIM/Documents/05. Dataset/Speech Recognition/raw/ECCC'
output_folder = 'output'

all_files = os.listdir(input_folder)
all_files = [f for f in all_files if f.endswith('.pdf')]
all_files = natsorted(all_files)

for file in all_files:
    folder_name = file.split('.')[0]
    os.makedirs(f'{output_folder}/{folder_name}/images', exist_ok=True)
    
    images = convert_from_path(f'{input_folder}/{file}')
    for i, image in enumerate(images):
        image.save(f'{output_folder}/{folder_name}/images/{i}.png', 'PNG')
    print(f'✅ - file {folder_name} done.')