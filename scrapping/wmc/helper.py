import requests
from bs4 import BeautifulSoup
from model import ContentModel, ArticleModel
from typing import Optional, List
import os
from tqdm import tqdm
import pandas as pd

def fetch_page_content(url_page: str) -> Optional[ContentModel]:
    try:
        html = requests.get(url_page).text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_='elementor-heading-title elementor-size-default').text.strip()
        contents = soup.find('div', attrs={'data-id': '3435bb92'}).find_all('p')
        audio_tag = soup.find('div', attrs={'data-id': '3435bb92'}).find('audio')
        audio = audio_tag.find('a')['href'] if audio_tag else None
        if not audio:
            return None
        save_content = ''
        for content in contents:
            if content.text:
                save_content += content.text + '\n'
        return ContentModel(title=title, content=save_content, audio=audio)
    except AttributeError as e:
        print(f"⚠️ Error processing the page: {e} 🤦‍♂️")
        return None
    except requests.exceptions.RequestException as e:
        print(f"🌐 Error fetching the page: {e} 📡")
        return None
    except Exception as e:
        print(f"❗ Unexpected error: {e} 🚨")
        return None


def get_links(page_number: int, base_url: str, logs: bool = True) -> List['ArticleModel']:
    if logs:
        os.makedirs('logs', exist_ok=True)
    url = f"{base_url}/{page_number}/"
    links = []
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find('div', class_='elementor-posts-container').find_all('article')
    for item in items:
        title = item.find('h3', class_='elementor-post__title').text if soup.find('h3', class_='elementor-post__title') else None
        date = item.find('div', class_='elementor-post__meta-data').find('span', class_='elementor-post-date').text if soup.find('div', class_='elementor-post__meta-data') else None
        author = item.find('div', class_='elementor-post__meta-data').find('span', class_='elementor-post-author').text if soup.find('div', class_='elementor-post__meta-data') else None
        link = item.find('a')['href'] if soup.find('a') else None
        title = title.strip() if title else None
        date = date.strip() if date else None
        author = author.strip() if author else None
        link = link.strip() if link else None
            
        model = ArticleModel(title=title, date=date, author=author, link=link if item else None)
        links.append(model)
    if logs:
        df = pd.DataFrame([link.model_dump() for link in links])
        df.to_csv(f'logs/{page_number}.csv', index=True)
    return links

def download_audio(url: str, output_path: str, filename: str):
    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, filename)
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    with open(file_path, 'wb') as file, tqdm(
        desc=filename,
        total=total_size_in_bytes,
        unit='B',
        unit_scale=True,
        bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}'
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

# base_url = 'https://wmc.org.kh/%e1%9e%96%e1%9f%90%e1%9e%8f%e1%9f%8c%e1%9e%98%e1%9e%b6%e1%9e%93%e1%9e%87%e1%9e%b6%e1%9e%8f%e1%9e%b7'
# start_from = 1
# end_at = 2
# links: ArticleModel = get_links(start_from, end_at, base_url)