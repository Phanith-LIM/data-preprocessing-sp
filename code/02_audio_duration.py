import os
from natsort import natsorted

input_folder = '/Users/PhanithLIM/Documents/05. Dataset/Speech Recognition/processing/aakanee'

folders = os.listdir(input_folder)
folders = [folder for folder in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, folder))]
folders = natsorted(folders)
list_duration = []

grand_total_duration = 0

for folder in folders:
    files = os.listdir(os.path.join(input_folder, folder))
    files = [f for f in files if f.endswith('.wav') or f.endswith('.mp3')]
    
    total_duration = 0
    for file in files:
        file_path = os.path.join(input_folder, folder, file)
        duration = os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"').read().strip()
        if duration:
            try:
                total_duration += float(duration)
            except ValueError:
                print(f"❌ - Invalid duration for {file}")
        else:
            print(f"❌ - Could not get duration for {file}")
    
    # Convert total_duration from seconds to hours, minutes, and seconds
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = int(total_duration % 60)
    grand_total_duration += total_duration
    print(f'✅ - {folder}: {hours} hours, {minutes} minutes, {seconds} seconds.')

grand_hours = int(grand_total_duration // 3600)
grand_minutes = int((grand_total_duration % 3600) // 60)
grand_seconds = int(grand_total_duration % 60)

print(f'\n🎉 Grand Total Duration: {grand_hours} hours, {grand_minutes} minutes, {grand_seconds} seconds.')