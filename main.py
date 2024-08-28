from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from requests import Session
import re
import gender_guesser.detector as gender
import pandas as pd

def fetch_articles_links(session: Session, page: int, headers: dict) -> set:
    root = 'https://cerncourier.com'
    url_rev = f'{root}/l/reviews'
    url = f'{url_rev}/page/{page}'
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.text, "html.parser")
    print(url)
    all_links = {link['href'] for link in soup.find_all('a', href=True)}
    specific_links = {link for link in all_links if link.startswith('https://cerncourier.com/a/')}
    return specific_links

def fetch_article_info(link: str, headers: dict) -> dict:
    
    req = requests.get(link, headers = headers)
    soup = BeautifulSoup(req.text, "html.parser")
    article_info: dict = {}
    try:
        article_info['title'] = soup.find("h1", class_= "single-header__heading").get_text(separator=" ").strip()
    except:
        article_info['title'] = "Not Found"

    try:
        article_info['date'] = soup.find("div", class_= "single-header__meta").get_text(separator=" ").strip()
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

def determine_gender(name: str, detector: gender.Detector) -> str:
    if name == "Not Found":
        gender = "unknown"
    else:
        gender = detector.get_gender(name.split()[0])
    
    return gender

if __name__== '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Encoding': 'utf-8'
    }
    page: int
    articles_urls = set()
    articles_info: list = []
    
    detector = gender.Detector()

    with requests.Session() as session:
        for page in range(1, 82):
            specific_links = fetch_articles_links(session, page, headers)
            articles_urls = articles_urls|specific_links
        print(articles_urls)
        for link in articles_urls:
            articles_info.append(fetch_article_info(link, headers))
        
        for article_info in articles_info:
            article_info['gender'] = determine_gender(article_info['author'], detector)
            print(article_info)

    df = pd.DataFrame(articles_info)
    df['date'] = pd.to_datetime(df['date'], format='%d %B %Y')

# Sort the DataFrame by the 'Date' column
    df_sorted = df.sort_values(by='date')
    df_sorted = df_sorted.drop(df.columns[[0, 1]], axis=1)
    df_sorted.to_csv("reviewers_gender.csv")
        
				
