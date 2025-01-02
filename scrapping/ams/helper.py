import requests
from bs4 import BeautifulSoup
from typing import Optional
import pandas as pd
import os
from tqdm import tqdm
from model import AMSArticleModel, LinkArticleModel
import ffmpeg  

def fetch_page_content(url_page: str) -> Optional[AMSArticleModel]:
    try:
        html = requests.get(url_page).text
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('h2', class_='article__title entry-title')
        title = title_tag.text.strip()
        
        date_tag = soup.find('time', class_='entry-date published').text
        
        category_tag = soup.find('div', class_='article__categories').find_all('a', attrs={'rel': 'category tag'})
        categories = [tag.text for tag in category_tag]
        
        audio_tag = soup.find('figure', class_='wp-block-audio')
        audio_src = audio_tag.find('audio').get('src') if audio_tag else 'No audio found'
        if(audio_src == 'No audio found'):
            return None
        
        content_div = soup.find('div', class_='article__content entry-content')
        p_tags = content_div.find_all('p') if content_div else []

        content = ''
        for p in p_tags:
            if p.find_parent('blockquote'):
                continue
            content += p.text.strip() + '\n'
            
        return AMSArticleModel(
            title=title, 
            audio_src=audio_src, 
            date=date_tag, 
            content=content, 
            categories=categories,
            url=url_page
        )
    except AttributeError as e:
        return None
    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None
    
        
def download_audio(url: str, output_path: str, filename: str):
    os.makedirs(output_path, exist_ok=True)
    if not filename.endswith('.ogg'):
        filename += '.ogg'
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
    print(f"Downloaded: {file_path}")
    convert_to_mp3(file_path, output_path)


def convert_to_mp3(input_file: str, output_path: str):
    mp3_file = os.path.join(output_path, os.path.basename(input_file).replace('.ogg', '.mp3'))
    try:
        ffmpeg.input(input_file).output(mp3_file, format='mp3').run()
        os.remove(input_file)
    except ffmpeg.Error as e:
        print(f"❗ Error during conversion: {e} 🚨")
    except Exception as e:
        print(f"❗ Unexpected error during conversion: {e} 🚨")

    
def get_links(page_number: int, base_url: str, logs: bool = True):
    url = f"{base_url}/{page_number}"
    links = []
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find('div', class_='articles').find_all('article')
    for item in items:
        id = item.get('id')
        title = item.find('div', class_='article__summary').find('h2').find('a').text
        url = item.find('div', class_='article__summary').find('h2').find('a').get('href')
        links.append(
            LinkArticleModel(
                id=id,
                title=title,
                url=url
            )   
        )
    return links



# if __name__ == '__main__':
#     url = 'https://education.ams.com.kh/education-update/national/news/do-young-people-who-read-a-lot-of-books-novels-and-motivational-literature-pose-a-problem-to-society'
#     article = fetch_page_content(url)
#     if article:
#         download_audio(article.audio_src, 'scrapping/ams/output', article.title)
#     else:
#         print("No audio found")
#     # links = get_links(1, 'https://education.ams.com.kh/category/all-news/news-life-education/page')
#     # print(links)