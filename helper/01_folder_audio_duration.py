import os
from natsort import natsorted
import subprocess
import statistics

input_folder = '/Users/PhanithLIM/Documents/05.Dataset/Speech Recognition/processing/WMC-Internation/output/13'
files = os.listdir(input_folder)
files = natsorted(files)
files = [f for f in files if f.endswith('.wav') or f.endswith('.mp3')]

list_duration = []
grand_total_duration = 0

for file in files:
    file_path = os.path.join(input_folder, file)
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duration = result.stdout.strip()
        
        if duration:
            total_duration = float(duration)
            list_duration.append(total_duration)
            grand_total_duration += total_duration
        else:
            print(f"❌ - Could not get duration for {file}")
    except Exception as e:
        print(f"❌ - Error processing {file}: {e}")

# Print results
print(f'✅ - Total files: {len(files)}')

grand_hours = int(grand_total_duration // 3600)
grand_minutes = int((grand_total_duration % 3600) // 60)
grand_seconds = int(grand_total_duration % 60)

print(f'\n🎉 Grand Total Duration: {grand_hours} hours, {grand_minutes} minutes, {grand_seconds} seconds.')

# Calculate and print statistics if there are valid durations
if list_duration:
    min_duration = min(list_duration)
    max_duration = max(list_duration)
    mean_duration = statistics.mean(list_duration)

    print(f'📊 Statistics:')
    print(f'   - Min Duration: {min_duration:.2f} seconds')
    print(f'   - Max Duration: {max_duration:.2f} seconds')
    print(f'   - Mean Duration: {mean_duration:.2f} seconds')
else:
    print("No valid durations found.")
