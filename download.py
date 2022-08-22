import os
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import requests
from clint.textui import progress
import re

get_soup = lambda url: BeautifulSoup(requests.get(url).text, 'html.parser')

def bib(soup, bib_path):
    url = 'http://libgen.is/book/' + soup.find('a', string='Link')['href']
    soup = get_soup(url)
    soup = soup.find('textarea', {'id': 'bibtext'})
    text = soup.text.strip().replace('book:', '')

    print('appending BibTeX entry to: ' + bib_path)
    with open(bib_path, 'a') as f:
        f.write(text.replace('\r\n', os.linesep))
        f.write('\n')

def fic(url, path):
    soup = get_soup(url)
    url = soup.find('a', string='Libgen.rs')['href']

    dl(url, path)

def non(url, bib_path, path):
    soup = get_soup(url)
    url = soup.find('a', string='this mirror')['href']

    bib(soup, bib_path) if bib_path else None
    dl(url, path)

def dl(url, path):
    file_name = lambda url: unquote(os.path.basename(urlparse(url).path))

    soup = get_soup(url)
    url = soup.find('a', string='GET')['href']

    file = file_name(url)
    file = path + file if path else file

    print('downloading: ' + file)
    r = requests.get(url, stream=True)
    with open(file, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
