import argparse
from pathlib import Path
import download
import populate

bib_path = None
dl_path = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='libgencli',
    description='download books from Library \
            Genesis')
    parser.add_argument('-g',
            choices=['fic', 'non'],
            default='fic',
            help='search fiction or non-fiction books')
    parser.add_argument('-d',
            metavar='DIR',
            type=str,
            help='save book to directory')
    parser.add_argument('-t',
            choices=['epub', 'mobi', 'azw', 'azw3', 'fb2', 'pdf', 'rtf', 'txt'],
            help='file type')
    parser.add_argument('-x',
            metavar='PATH',
            type=str,
            help='append BibTeX entry to file at path')
    parser.add_argument('query',
            type=str,
            nargs='+',
            help='search query')
    args = parser.parse_args()

    if args.d:
        path = Path(args.d)
        if path.is_dir():
            dl_path = args.d + '/'
            dl_path = dl_path.replace('//', '/')
        else:
            print('error: invalid directory')
            exit(0)

    if args.x:
        path = Path(args.x)
        if not path.is_file():
            print('error: invalid BibTeX file')
            exit(0)
        else:
            bib_path = args.x

    if args.g == 'non':
        url = 'https://libgen.is/search.php?req='
    else:
        # build fiction url
        pass

    for word in args.query:
        url += word + '+'

    if args.g == 'non':
        url = url[:-1] + '&res=100'
        books = populate.non(url)
    else:
        pass
        # build fiction books

    # filter books by filetype
    if args.t:
        foo = []
        for book in books:
            foo.append(book) if book.ext == args.t else None
        books = foo

    if len(books) == 0:
        print('no books found.')
        exit(0)

    for i, book in enumerate(books):
        print(i, '(BOOK #)')
        book.print()
        print()

    # book selection loop
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

    url = books[sel_num].url
    if args.g == 'non':
        download.non(url, bib_path, dl_path)
    else:
        pass
        # fiction download
