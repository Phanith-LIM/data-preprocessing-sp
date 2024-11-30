import requests
from tqdm import tqdm

def download_audio(url: str, filename: str):
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size_in_bytes,
        unit='B',
        unit_scale=True,
        bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}'
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

# Example usage
url = 'https://wmc.org.kh/wp-content/uploads/2024/11/vattey28-11-24.mp3-Completed.mp3'
filename = '../../'

download_audio(url, filename)
