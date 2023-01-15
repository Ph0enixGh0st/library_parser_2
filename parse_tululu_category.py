import argparse, logging, os, time
import pickle, requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.error import HTTPError
from urllib.parse import urljoin


n = 0

#  https://tululu.org/l55/2/
url = 'https://tululu.org/l55/'
book_page = requests.get(url)
book_page.raise_for_status()
soup = BeautifulSoup(book_page.text, 'lxml')
#book_short_link = soup.select_one('div.bookimage a').get('href')
#full_link = urljoin(f'https://tululu.org/l55/', book_short_link)
links = soup.find_all('div', class_='bookimage')
for link in links:
    n += 1
    short_link = urljoin(f'https://tululu.org/l55/', link.find('a').attrs['href'])
    print(n, short_link)

for page in range (1, 11):
    url = f'https://tululu.org/l55/{page}'
    book_page = requests.get(url)
    book_page.raise_for_status()
    soup = BeautifulSoup(book_page.text, 'lxml')

    links = soup.find_all('div', class_='bookimage')
    for link in links:
        n += 1
        short_link = urljoin(f'https://tululu.org/l55/', link.find('a').attrs['href'])
        print(n, short_link)





