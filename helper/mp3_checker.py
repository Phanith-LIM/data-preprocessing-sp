import os
from pydub.utils import mediainfo
import os
from natsort import natsorted
from prettytable import PrettyTable




def check_mp3(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        return True  # Return True if file does not exist (error case)

    try:
        # Get media info using pydub
        info = mediainfo(file_path)
        if info.get('codec_name') == 'mp3':
            return False  # Return False if file is a valid MP3
        else:
            return True  # Return True if the file is not a valid MP3
    except Exception as e:
        return True
    
path = 'output'
table = PrettyTable()
table.field_names = ["folder", "filename"]
folders = os.listdir(path)
folders = [f for f in folders if f.endswith('.mp3')]
folders = natsorted(folders)
print(folders)

# for file in folder:
#     file_path = os.path.join(folders, file)
#     if check_mp3(file_path):
#         print(f'{file} is not a valid MP3 file')
#     else:
#         print(f'{file} is a valid MP3 file')