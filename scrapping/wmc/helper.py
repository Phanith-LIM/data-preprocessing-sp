import requests
from bs4 import BeautifulSoup
from model import ContentModel, ArticleModel
from typing import Optional, List
import os
import json
from tqdm import tqdm
import pandas as pd

def fetch_page_content(url_page: str) -> Optional[ContentModel]:
    try:
        html = requests.get(url_page).text
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('h2', class_='elementor-heading-title elementor-size-default')
        title = title_tag.text.strip()
    
        if not title:
            print(f"⚠️ Skipping article: Title not found.")
            return None

        # content_div = soup.find('div', attrs={'data-id': '3435bb92'}) / 1 - 180
        content_div = soup.find('div', attrs={'data-id': '3435bb92'})
        if not content_div:
            print(f"⚠️ Skipping article: Content div not found.")
            return None

        contents = content_div.find_all('p')
        save_content = ''
        for content in contents:
            if content.get('style') == 'text-align: center':
                continue
            if content.text.strip():
                save_content += content.text.strip() + '\n'
                
        
        audio = None
        audio_tag = content_div.find('audio')
        if audio_tag and audio_tag.find('a'):
            audio = audio_tag.find('a')['href']
        else:
            figure_audio = content_div.find('figure', class_='wp-block-audio')
            if figure_audio:
                audio_tag = figure_audio.find('audio')
                if audio_tag and audio_tag.has_attr('src'):
                    audio = audio_tag['src']
                    
        if audio and audio.startswith("blob:"):
            audio = audio.replace("blob:", "")
            
        if not audio:
            script_tag = soup.find('script', class_='wp-playlist-script', type='application/json')
            if script_tag:
                try:
                    json_data = json.loads(script_tag.string)
                    tracks = json_data.get('tracks', [])
                    if tracks:
                        audio = tracks[0].get('src', None) 
                except json.JSONDecodeError as e:
                    print(f"⚠️ Error decoding JSON from <script> tag: {e}")
                    
        if audio and audio.startswith("blob:"):
            audio = audio.replace("blob:", "")
            
        if not audio:
            return None
        
        return ContentModel(title=title, content=save_content.strip(), audio=audio)

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
        title = item.find('h3', class_='elementor-post__title').text
        date = item.find('div', class_='elementor-post__meta-data').find('span', class_='elementor-post-date').text
        author = item.find('div', class_='elementor-post__meta-data').find('span', class_='elementor-post-author').text
        link = item.find('a')['href']
        title = title.strip()
        date = date.strip()
        author = author.strip()
        link = link.strip()
            
        model = ArticleModel(title=title, date=date, author=author, link=link)
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
    with open(file_path, 'wb') as file, tqdm(desc=filename, total=total_size_in_bytes, unit='B', unit_scale=True, bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}') as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))
            
data: Optional[ContentModel] = fetch_page_content('https://wmc.org.kh/article/85092/%e1%9e%9f%e1%9e%98%e1%9f%92%e1%9e%8a%e1%9f%81%e1%9e%85%e1%9e%a0%e1%9f%8a%e1%9e%bb%e1%9e%93%e1%9e%9f%e1%9f%82%e1%9e%93%e1%9e%85%e1%9f%92%e1%9e%9a%e1%9e%b6%e1%9e%93%e1%9e%85%e1%9f%84%e1%9e%9b%e1%9e%96/')
print(data)