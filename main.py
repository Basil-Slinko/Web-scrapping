import requests
from bs4 import BeautifulSoup


def find_articles(key_words):
    request = requests.get('https://habr.com/ru/all/')
    soup = BeautifulSoup(request.text, 'html.parser')
    posts = soup.find_all('article', class_='tm-articles-list__item')

    for post in posts:
        post_text = post.find('div', class_=['article-formatted-body article-formatted-body_version-2',
                                             'article-formatted-body article-formatted-body_version-1'])

        time_article = post.find('time')
        date_time_article = time_article.get('title')

        title_article = post.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2')

        url_article = post.find('a', class_='tm-article-snippet__title-link')
        link_href = url_article.get('href')
        url_article_full = f'https://habr.com{link_href}'

        hubs = post.find_all('a', class_='tm-article-snippet__hubs-item-link')
        hubs_text = ''
        for hub in hubs:
            hubs_text += f' {hub.span.contents[0]}'

        post_preview = post_text.find_all(["p", "br"])
        post_preview_str = ''
        for indent in post_preview:
            post_preview_str += str(indent)

        preview_article_str = f'{title_article.a.span.contents[0].text}{hubs_text}{post_preview_str}'

        for key_word in key_words:
            if key_word not in preview_article_str.lower():
                continue
            else:
                print(f'{date_time_article} — {title_article.a.span.contents[0]} — \n{url_article_full}\n')
            break


if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    find_articles(KEYWORDS)
