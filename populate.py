import requests
from bs4 import BeautifulSoup
import main
import re

books = []

class Book:
    def __init__(self):
        self.author = ''
        self.title = ''
        self.series = ''
        self.year = ''
        self.ext = ''
        self.pub = ''
        self.isbn = ''
        self.url = ''

    def print(self):
        exists = lambda entry: True if entry != '' else False

        print(self.title) if exists(self.title) else None
        print(self.author) if exists(self.author) else None
        print('series: ' + self.series) if exists(self.series) else None
        print('publisher: ' + self.pub) if exists(self.pub) else None

        info = ''
        info += self.year + ', ' if self.year != '' else ''
        info += self.ext + ', ' if self.ext != '' else ''
        info += 'ISBN: ' + self.isbn + ', ' if self.isbn != '' else ''
        print(info[:-2]) if info != '' else None

get_soup = lambda url: BeautifulSoup(requests.get(url).text, 'html.parser')
parse_basic = lambda soup: soup.text.strip()

def fic(url):
    soup = get_soup(url)
    table = soup.find('table', {'class': 'catalog'})

    i = 0
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

                url = 'https://libgen.is' + title_soup['href']
                books[i].url = url

                reg = re.compile('^ISBN')
                isbn_soup = col.find('p', string=reg)
                if isbn_soup:
                    isbn = parse_basic(isbn_soup).replace('ISBN: ', '')
                    books[i].isbn = isbn
            elif (j == 4):
                ext = col.text
                ext = ext.split(' /')[0].lower()
                books[i].ext = ext

            j += 1

        i += 1

    return books

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
                reg = re.compile('^\d{9,}')
                isbn_soup = col.find('i', string=reg)
                if (isbn_soup):
                    isbn = parse_basic(isbn_soup)
                    books[i].isbn = isbn

                reg = re.compile('^search')
                series_soup = col.find('a', href=reg)
                if series_soup:
                    books[i].series = parse_basic(series_soup)

                reg = re.compile('^book')
                title_soup = col.find('a', href=reg)
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

if __name__ == '__main__':
    # url = 'https://libgen.is/fiction/?q=adventurers+wanted'
    # fic(url)
    url = 'http://libgen.is/search.php?req=lewis+vaughn&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def'
    non(url)

    for i, book in enumerate(books):
        print(i, '(BOOK #)')
        book.print()
        print()
