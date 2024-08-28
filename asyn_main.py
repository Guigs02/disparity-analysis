import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from requests import Session
import re
import gender_guesser.detector as gender

async def fetch_articles_links(session: aiohttp.ClientSession, page: int, headers: dict) -> set:
    root = 'https://cerncourier.com'
    url = f'{root}/l/reviews/page/{page}'
    async with session.get(url, headers=headers) as response:
        soup = BeautifulSoup( await response.text(), "html.parser")
        print(url)
        all_links = {link['href'] for link in soup.find_all('a', href=True)}
        specific_links = {link for link in all_links if link.startswith('https://cerncourier.com/a/')}
        return specific_links

async def fetch_article_info(session: aiohttp.ClientSession, link: str, headers: dict) -> dict:
    article_info: dict = {
        'title': "",
        'date': "",
        'link': "",
        'author': "",
        'gender': ""
}
    async with session.get(link, headers=headers) as response:
        soup = BeautifulSoup( await response.text(), "html.parser")
        try:
            article_info['title'] = soup.find("h1", class_= "single-header__heading").get_text()
        except:
            article_info['title'] = "Not Found"

        try:
            article_info['date'] = soup.find("div", class_= "single-header__meta").get_text()
        except:
            article_info['date'] = "Not Found"
            
        author_div = soup.find("div", class_= "author-byline")
        if author_div is not None:
            article_info['author'] = author_div.get_text(separator=" ").strip()
            #print(detector.get_gender(articles_info['author'].split()[0]))
        else:
            article_info['author'] = "Not Found"
        print(article_info['author'])
        
        return article_info

def determine_gender(article_info: dict, detector: gender.Detector) -> None:
    if article_info['author'] == "Not Found":
        article_info['gender'] = "Unknown"
    else:
        article_info['gender'] = detector.get_gender(article_info['author'].split()[0])
    
    return 

async def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Encoding': 'utf-8'
    }
    articles_urls = set()
    articles_info: list = []
    tasks: list = []
    info_tasks: list = []
    gender_tasks: list = []
    
    detector = gender.Detector()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_articles_links(session, page, headers) for page in range(1, 82)]
        urls = await asyncio.gather(*tasks)
        print(len(urls))
        print(urls)
        for links in urls:
            articles_urls.update(links)
        print(urls)

        info_tasks = [fetch_article_info(session, link, headers) for link in articles_urls]
        articles_info.append(await asyncio.gather(*info_tasks))

        for article_info in articles_info[0]:
            determine_gender(article_info, detector)
    


    print(articles_info)
    i=0
    for article_info in articles_info[0]:
        print(article_info)
        i+=1
    print(i)
if __name__== '__main__':
   asyncio.run(main())
