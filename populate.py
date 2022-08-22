import requests
from bs4 import BeautifulSoup
import main
import re

books = []
page = 1

class Book:
    def __init__(self):
        self.author = ''
        self.title = ''
        self.series = ''
        self.year = ''
        self.ext = ''
        self.pub = ''
        self.isbn = ''
        self.doi = ''
        self.journ = ''
        self.vol = ''
        self.iss = ''
        self.url = ''

    def print(self):
        exists = lambda entry: True if entry != '' else False

        print(self.title) if exists(self.title) else None
        print(self.author) if exists(self.author) else None
        print('series: ' + self.series) if exists(self.series) else None
        print('publisher: ' + self.pub) if exists(self.pub) else None
        print('journal: ' + self.journ) if exists(self.journ) else None
        print(self.doi) if exists(self.doi) else None

        info = ''
        info += self.year + ', ' if self.year != '' else ''
        info += 'vol. ' + self.vol + ', ' if self.vol != '' else ''
        info += 'iss. ' + self.iss + ', ' if self.iss != '' else ''
        info += self.ext + ', ' if self.ext != '' else ''
        info += 'ISBN: ' + self.isbn + ', ' if self.isbn != '' else ''
        print(info[:-2]) if info != '' else None

get_soup = lambda url: BeautifulSoup(requests.get(url).text, 'html.parser')
parse_basic = lambda soup: soup.text.strip()

def sci(url):
    soup = get_soup(url)

    if soup.find('p', string='No articles were found.'):
        return books

    table = soup.find('table', {'class': 'catalog'})

    i = len(books)
    for row in table.find_all('tr')[1:]:
        books.append(Book())
        j = 0
        for col in row.find_all('td'):
            if (j == 0):
                books[i].author = parse_basic(col)
            elif (j == 1):
                data_soups = col.find_all(text=True)
                data = ''
                for soup in data_soups[1:]:
                    data += parse_basic(soup) + ' '

                p = re.compile('DOI:\s(.+)$')
                r = p.search(data)
                doi = r.group(0)
                books[i].doi = doi.strip()
                books[i].title = data.replace(doi, '').strip()

                books[i].url = 'https://libgen.is' + col.find('a')['href']

            elif (j == 2):
                journ_soup = col.find('a', href=True)
                books[i].journ = parse_basic(journ_soup)

                data_soup = col.select('a + p')[0]
                data = parse_basic(data_soup)

                # return data given regular expression
                def get_data(reg):
                    p = re.compile(reg)
                    r = p.search(data)
                    return r.group(1) if r else ''

                books[i].vol = get_data('volume\s(\d+)')
                books[i].iss = get_data('issue\s(\d+)')
                books[i].year = get_data('\((\d+)\)')

            j += 1

        i += 1

    global page
    page += 1
    url = url[:-1] + str(page)
    return sci(url)

def fic(url):
    soup = get_soup(url)

    if soup.find('p', string='No files were found.'):
        return books

    table = soup.find('table', {'class': 'catalog'})

    i = len(books)
    for row in table.find_all('tr')[1:]:
        books.append(Book())
        j = 0
        for col in row.find_all('td'):
            if (j == 0):
                books[i].author = parse_basic(col)
            elif (j == 1):
                books[i].series = parse_basic(col)
            elif (j == 2):
                title_soup = col.find('a')
                books[i].title = parse_basic(title_soup)

                book_url = 'https://libgen.is' + title_soup['href']
                books[i].url = book_url

                r = re.compile('^ISBN')
                isbn_soup = col.find('p', string=r)
                if isbn_soup:
                    isbn = parse_basic(isbn_soup).replace('ISBN: ', '')
                    books[i].isbn = isbn
            elif (j == 4):
                ext = col.text
                ext = ext.split(' /')[0].lower()
                books[i].ext = ext

            j += 1

        i += 1

    global page
    page += 1
    url = url[:-1] + str(page)
    return fic(url)

def non(url):
    soup = get_soup(url)
    table = soup.find('table', {'class': 'c'})

    i = 0
    for row in table.find_all('tr')[1:]:
        books.append(Book())
        j = 0
        for col in row.find_all('td'):
            if (j == 1):
                books[i].author = parse_basic(col)
            elif (j == 2):
                r = re.compile('^\d{9,}')
                isbn_soup = col.find('i', string=r)
                if (isbn_soup):
                    isbn = parse_basic(isbn_soup)
                    books[i].isbn = isbn

                r = re.compile('^search')
                series_soup = col.find('a', href=r)
                if series_soup:
                    books[i].series = parse_basic(series_soup)

                r = re.compile('^book')
                title_soup = col.find('a', href=r)
                books[i].title = parse_basic(title_soup).replace(isbn, '')

                url = 'https://libgen.is/' + title_soup['href']
                books[i].url = url
            elif (j == 3):
                books[i].pub = parse_basic(col)
            elif (j == 4):
                books[i].year = parse_basic(col)
            elif (j == 8):
                books[i].ext = parse_basic(col)

            j += 1

        i += 1

    return books
