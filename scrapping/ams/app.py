from model import AMSArticleModel, LinkArticleModel
from typing import List
from helper import get_links, fetch_page_content, download_audio
import os
import pandas as pd

base_url = 'https://education.ams.com.kh/category/all-news/news-national-and-international-education-update/news-national-education/page'
output_path = '/Users/PhanithLIM/Documents/04.Projects/data-preprocessing-sp/scrapping/ams/output'
start_from = 110
end_at = 226

for page_number in range(start_from, end_at + 1):
    links: List[LinkArticleModel] = get_links(page_number=page_number, base_url=base_url)
    os.makedirs(f'{output_path}/{page_number}', exist_ok=True)
    print("PAGE: ", page_number)
    list_article = []
    for index, article_url in enumerate(links):
        article: AMSArticleModel = fetch_page_content(article_url.url)
        if(article is None):
            print(f'[{index}] not audio found.')
            continue
        list_article.append({
            'post_id': article_url.id,
            'title': article.title,
            'date': article.date,
            'categories': article.categories,
            'audio_src': article.audio_src,
            'url': article.url
        })
        download_audio(article.audio_src, f'{output_path}/{page_number}', f'{index}.ogg')
        print(f'[{index}] {article.title} downloaded.')
        with open(f'{output_path}/{page_number}/{index}.txt', 'w') as text_file:
            text_file.write(article.content)
    df = pd.DataFrame(list_article)
    df.to_csv(f'/Users/PhanithLIM/Documents/04.Projects/data-preprocessing-sp/scrapping/ams/logs/{page_number}.csv', index=True)  