import requests
from bs4 import BeautifulSoup
from MainPage.models import Anime, Movie, Manga
#from translate import Translator
import time
import re
import random


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36"
]

headers = {
    "User-Agent": random.choice(user_agents)
}


def clean_html_tags(text):
    clean = re.sub(r'<.*?>', '', text)
    return clean.strip()


def parse_anime_site():
    for i in range(0, 27650, 50): #Всего 27650
        page = requests.get('https://myanimelist.net/topanime.php?limit='+str(i))
        soup = BeautifulSoup(page.text, "html.parser")
        anime_list = soup.find_all('tr', class_='ranking-list')
        for anime in anime_list:

            title_tag = anime.find('h3', class_='anime_ranking_h3')
            title = title_tag.text.strip() if title_tag else "No Title"
            title_clean = clean_html_tags(title)

            score_tag = anime.find('div', class_='js-top-ranking-score-col')
            rating = score_tag.text.strip() if score_tag else None

            img_tag = anime.find('img')
            img_url = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else None

            url_tag = anime.find('a', class_='hoverinfo_trigger')
            url = url_tag['href'] if url_tag else None

            info_tag = anime.find('div', class_='information di-ib mt4')
            season = info_tag.text.strip() if info_tag else None

            Anime.objects.create(
                title=title_clean,
                rating=rating,
                img=img_url,
                url=url,
                season=season
            )

            print(f"Добавлено аниме: {title} - {rating}")


def parse_film_site():
    for i in range(1, 692):
        time.sleep(3)
        page = requests.get(f'https://www.kinopoisk.ru/top/navigator/m_act[egenre]/1750/order/rating/page/{i}/#results', headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        movie_list = soup.find_all('div', class_='item _NO_HIGHLIGHT_')
        print(i)
        for movie in movie_list:

            name_div = movie.find('div', class_='name')
            title_tag = name_div.find('a') if name_div else None
            title = title_tag.text.strip() if title_tag else "No Title"
            title_clean = clean_html_tags(title)

            year_tag = movie.find('div', class_='name').find_next('span')
            year = year_tag.text.strip() if year_tag else "Unknown Year"

            score_tag = movie.find('div', class_='imdb')
            rating = score_tag.text.strip() if score_tag else None

            img_tag = movie.find('img')
            img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

            Movie.objects.create(
                title=title_clean,
                rating=rating,
                img=img_url,
                year=year,
            )

            print(f"Добавлен фильм: {title_clean} - {rating}")


def parse_mangabuff():
    for i in range(1, 198): #198
        time.sleep(3)
        page = requests.get(f'https://mangabuff.ru/manga?page={i}')
        soup = BeautifulSoup(page.text, "html.parser")
        manga_list = soup.find_all('a', class_='cards__item')
        for manga in manga_list:
            print("YES")
            title_tag = manga.find('div', class_='cards__name')
            title = title_tag.text.strip() if title_tag else "No Title"
            title_clean = clean_html_tags(title)

            type_tag = manga.find('div', class_='cards__info')
            type = type_tag.text.strip() if type_tag else None


            rating_tag = manga.find('span', class_='cards__rating cards__rating--green')
            rating = rating_tag.text.strip() if rating_tag else None

            base_url = 'https://mangabuff.ru'
            img_div = manga.find('div', class_='cards__img')
            img_url = None
            if img_div and 'style' in img_div.attrs:
                style = img_div['style']
                import re
                match = re.search(r"url\('(.*?)'\)", style)
                if match:
                    relative_img_url = match.group(1)
                    img_url = f"{base_url}{relative_img_url}"

            Manga.objects.create(
                title=title_clean,
                rating=rating,
                img=img_url,
                type=type,
            )

            print(f"Добавлен тайтл: {title_clean} - {rating}")


def parse_lord_film():
    for i in range(1, 553):
        time.sleep(3)
        page = requests.get(f'https://mm.lordfilm15.ru/filmy/page/{i}/')
        soup = BeautifulSoup(page.text, "html.parser")
        movie_list = soup.find_all('div', class_='th-item')
        for movie in movie_list:

            title_tag = movie.find('div', class_='th-title')
            title = title_tag.text.strip() if title_tag else "No Title"
            title_clean = clean_html_tags(title)

            score_tag = movie.find('div', class_='th-rate th-rate-imdb')
            rating = score_tag.find('span').text.strip() if score_tag else None

            img_tag = movie.find('img')
            img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
            base_url = 'https://mm.lordfilm15.ru'
            img = f'{base_url}{img_url}'

            Movie.objects.create(
                title=title_clean,
                rating=rating,
                img=img,
            )

            print(f"Добавлен фильм: {title_clean} - {rating}")