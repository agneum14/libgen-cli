import argparse
from pathlib import Path
import download
import populate

bib_path = None
dl_path = None
books = []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='libgencli',
    description='download books from Library \
            Genesis')
    parser.add_argument('-g',
            choices=['fic', 'non', 'sci'],
            default='non',
            help='search fiction or non-fiction books')
    parser.add_argument('-d',
            metavar='DIR',
            type=str,
            help='save book to directory')
    parser.add_argument('-t',
            choices=['epub', 'mobi', 'azw', 'azw3', 'fb2', 'pdf', 'rtf', 'txt'],
            help='filter by file type')
    parser.add_argument('-i',
            metavar = 'ISBN',
            type=str,
            help='filter by ISBN')
    parser.add_argument('-x',
            metavar='PATH',
            type=str,
            help='append BibTeX entry to file at path')
    parser.add_argument('query',
            type=str,
            nargs='+',
            help='search query')
    args = parser.parse_args()

    # validate download directory
    if args.d:
        path = Path(args.d)
        if path.is_dir():
            dl_path = args.d + '/'
            dl_path = dl_path.replace('//', '/')
        else:
            print('error: invalid directory')
            exit(0)

    # validate BibTex file
    if args.x:
        path = Path(args.x)
        if not path.is_file():
            print('error: invalid BibTeX file')
            exit(0)
        else:
            bib_path = args.x

    # set initial search url by genre
    if args.g == 'non':
        url = 'https://libgen.is/search.php?req='
    elif args.g == 'fic':
        url = 'https://libgen.is/fiction/?q='
    elif args.g == 'sci':
        url = 'https://libgen.is/scimag/?q='

    # append query to search url
    for word in args.query:
        url += word + '+'

    # complete search url, get books
    if args.g == 'non':
        url = url[:-1] + '&res=100'
        books = populate.non(url)
    elif args.g == 'fic':
        url = url[:-1] + '&page=1'
        books = populate.fic(url)
    elif args.g == 'sci':
        url = url[:-1] + '&page=1'
        books = populate.sci(url)

    # filter books by file type
    if args.t:
        foo = []
        for book in books:
            foo.append(book) if book.ext == args.t else None
        books = foo

    # filter books by ISBN
    if args.i:
        foo = []
        for book in books:
            foo.append(book) if args.i in book.isbn else None
        books = foo

    # exit if no books
    if len(books) == 0:
        print('no books found.')
        exit(0)

    # display books
    for i, book in enumerate(books):
        print(i, '(BOOK #)')
        book.print()
        print()

    # loop book selection
    while True:
        sel = input('enter BOOK # (-1 terminates): ')
        if sel == '-1':
            print('terminated.')
            exit(0)
        if not sel.isdigit():
            print('error: expected int')
            continue

        sel_num = int(sel)
        if sel_num < 0 or sel_num >= len(books):
            print('error: selection outside range')
            continue

        break

    url = books[sel_num].url # book url

    # download book
    if args.g == 'non':
        download.non(url, bib_path, dl_path)
    elif args.g == 'fic':
        download.fic(url, dl_path)
    elif args.g == 'sci':
        download.sci(url, bib_path, dl_path)
