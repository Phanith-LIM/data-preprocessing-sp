from model import ArticleModel, ContentModel
from helper import get_links, fetch_page_content, download_audio
from typing import List, Optional
import os

base_url = 'https://wmc.org.kh/%e1%9e%96%e1%9f%90%e1%9e%8f%e1%9f%8c%e1%9e%98%e1%9e%b6%e1%9e%93%e1%9e%87%e1%9e%b6%e1%9e%8f%e1%9e%b7/'
output_path = 'output'
start_from = 405
end_at = 539

for index in range(start_from, end_at + 1):
    print(f'\n🔍 **Fetching Page {index}**')
    articles: List[ArticleModel] = get_links(page_number=index, base_url=base_url)
    os.makedirs(f'{output_path}/{index}', exist_ok=True)
    for file, article in enumerate(articles):
        meta: Optional[ContentModel] = fetch_page_content(article.link)
        if meta is None:
            print(f'⚠️ Skipped article {file}: Required metadata not found.')
            continue
        if(meta.audio == None):
            print(f'⚠️ Skipped article {file}: Required metadata not found.')
            continue
        text_file_path = f'{output_path}/{index}/{file}.txt'
        with open(text_file_path, 'w') as text_file:
            text_file.write(meta.content)
        print(f'{file}.txt')

        if meta.audio:
            audio_file_name = f'{file}.mp3'
            download_audio(meta.audio, f'{output_path}/{index}', audio_file_name)
        print()
    print(f'✅ **Page {index} has been downloaded successfully.**\n')

