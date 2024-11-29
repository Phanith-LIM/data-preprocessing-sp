import os
from natsort import natsorted
from pdf2image import convert_from_path

all_files = os.listdir('data/ECCC')
all_files = [f for f in all_files if f.endswith('.pdf')]
all_files = natsorted(all_files)

input_folder = 'data/ECCC'
output_folder = 'output/ECCC'

for file in all_files:
    folder_name = file.split('.')[0]
    os.makedirs(f'{output_folder}/{folder_name}', exist_ok=True)
    
    images = convert_from_path(f'{input_folder}/{file}')
    for i, image in enumerate(images):
        image.save(f'{output_folder}/{folder_name}/{i}.png', 'PNG')
    print(f'✅ - {folder_name} done.')