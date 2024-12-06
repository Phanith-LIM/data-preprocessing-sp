import os
from natsort import natsorted
import pandas as pd

# Paths
path = '/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/output'
path_logs = '/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/logs'

folders = os.listdir(path)
folders = [folder for folder in folders if not folder.startswith('.')]
folders = natsorted(folders)

for folder in folders:
    folder_path = os.path.join(path, folder)
    files = os.listdir(folder_path)
    files = [file for file in files if file.endswith(('.txt', '.mp3'))]
    files = natsorted(files)
    file_names = {os.path.splitext(file)[0] for file in files}
    path_log = os.path.join(path_logs, f"{folder}.csv")

    # Read CSV
    if os.path.exists(path_log):
        df = pd.read_csv(path_log, sep=',')
        df = df.rename(columns={'Unnamed: 0': 'id'})
        df_filtered = df[df['id'].astype(str).isin(file_names)]
        df_filtered.to_csv(path_log, index=False)
        print(f"Updated {path_log}: {len(df_filtered)} rows kept.")
