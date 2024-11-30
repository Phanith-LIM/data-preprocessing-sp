import os
from natsort import natsorted
import statistics

input_folder = '/Users/PhanithLIM/Documents/04. Projects/data-preprocessing-sp/data/output'
folders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
folders = natsorted(folders)
list_duration = []

grand_total_duration = 0
grand_text_count = 0
grand_audio_count = 0

for folder in folders:
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
                list_duration.append(duration_float)  # Add duration to the list
            except ValueError:
                print(f"❌ - Invalid duration for {file}")
        else:
            print(f"❌ - Could not get duration for {file}")
    
    # Convert total_duration from seconds to hours, minutes, and seconds
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = int(total_duration % 60)
    grand_total_duration += total_duration
    grand_text_count += text_count
    grand_audio_count += audio_count
    print(f'✅ - {folder}: {hours} hours, {minutes} minutes, {seconds} seconds.')
    
grand_hours = int(grand_total_duration // 3600)
grand_minutes = int((grand_total_duration % 3600) // 60)
grand_seconds = int(grand_total_duration % 60)

# Compute min, max, and mean durations
if list_duration:
    min_duration = min(list_duration)
    max_duration = max(list_duration)
    mean_duration = statistics.mean(list_duration)

    print(f'\n🎉 Grand Total Duration: {grand_hours} hours, {grand_minutes} minutes, {grand_seconds} seconds.')
    print(f'📊 Statistics:')
    print(f'   - Min Duration: {min_duration:.2f} seconds')
    print(f'   - Max Duration: {max_duration:.2f} seconds')
    print(f'   - Mean Duration: {mean_duration:.2f} seconds')
    print('\n')
    print(f'   - Total Text Files: {grand_text_count}')
    print(f'   - Total Audio Files: {grand_audio_count}')
else:
    print("\nNo valid durations found.")
