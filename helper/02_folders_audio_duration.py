import os
import numpy as np
from natsort import natsorted
import pandas as pd
from datetime import datetime
from prettytable import PrettyTable
input_folder = '/Users/PhanithLIM/Documents/04.Projects/data-preprocessing-sp/scrapping/ams/output'
folders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
folders = natsorted(folders)

# Initialize table
table = PrettyTable()
table.field_names = ["Folder", "Duration"]
table.align["Duration"] = "l"

# Variables for summary
list_duration = []
meta_data = []
grand_total_duration = 0
grand_text_count = 0
grand_audio_count = 0

list_error = []

# Process each folder
for i, folder in enumerate(folders, 1):
    folder_path = os.path.join(input_folder, folder)
    files = os.listdir(folder_path)

    # Count text and audio files
    text_files = [f for f in files if f.endswith('.txt')]
    audio_files = [f for f in files if f.endswith('.wav') or f.endswith('.mp3')]

    text_count = len(text_files)
    audio_count = len(audio_files)

    total_duration = 0
    for file in audio_files:
        file_path = os.path.join(folder_path, file)
        duration = os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"').read().strip()
        if duration:
            try:
                duration_float = float(duration)
                total_duration += duration_float
                list_duration.append(duration_float)
            except ValueError:
                body = {
                    "Folder": folder,
                    "File": file,
                }
                list_error.append(body)
                print(f"❌ - Invalid duration for {file}")
        else:
            print(f"❌ - Could not get duration for {file}")
            
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = int(total_duration % 60)
    duration_str = f"{hours}h {minutes}m {seconds}s"

    # Update summary
    grand_total_duration += total_duration
    grand_text_count += text_count
    grand_audio_count += audio_count
    body = {
        "Folder": folder,
        "Duration": duration_str,
    }
    meta_data.append(body)
    table.add_row([folder, duration_str])
    os.system('clear')
    print(f"✅ - {folder}: {duration_str}\n")
    print(table)

# Grand summary
grand_hours = int(grand_total_duration // 3600)
grand_minutes = int((grand_total_duration % 3600) // 60)
grand_seconds = int(grand_total_duration % 60)

if list_duration:
    min_duration = min(list_duration)
    max_duration = max(list_duration)
    mean_duration = np.mean(list_duration)

    # Convert durations from seconds to h, m, s
    def format_duration(duration):
        h = int(duration // 3600)
        m = int((duration % 3600) // 60)
        s = int(duration % 60)
        return f"{h}h {m}m {s}s"

    min_duration_str = format_duration(min_duration)
    max_duration_str = format_duration(max_duration)
    mean_duration_str = format_duration(mean_duration)

    print(f"\n🎉 Grand Total Duration: {grand_hours}h {grand_minutes}m {grand_seconds}s")
    print(f"📊 Minimum Duration: {min_duration_str}")
    print(f"📊 Maximum Duration: {max_duration_str}")
    print(f"📊 Mean Duration: {mean_duration_str}")
    
    df = pd.DataFrame(list_error)
    df.to_csv('logs/error_duration.csv', index=False)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    df = pd.DataFrame(meta_data)
    df.to_csv(f'logs/metadata_{timestamp}.csv', index=False)
else:
    print("\nNo audio files found.")
