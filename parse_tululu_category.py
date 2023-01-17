import argparse, logging, os, time
import json, requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.error import HTTPError
from urllib.parse import urljoin


def check_for_redirect(book_page):
    if book_page.history:
        raise requests.exceptions.HTTPError


def make_soup(book_link):

    book_page = requests.get(book_link)
    book_page.raise_for_status()
    soup = BeautifulSoup(book_page.text, 'lxml')
    check_for_redirect(book_page)

    return soup


def get_book_link_credentials(soup, book_link):

    book_credentials = []

    book_title_author = soup.select_one('.ow_px_td h1').text
    title, author = book_title_author.split(' \xa0 :: \xa0 ')

    book_pic_link = soup.select_one('div.bookimage img')['src']
    book_pic_link = urljoin(book_link, book_pic_link)

    book_download_link = soup.select('table.d_book a')[8].get('href')
    book_download_link = urljoin(book_link, book_download_link)

    book_credentials.append(book_download_link)
    book_credentials.append(title)
    book_credentials.append(book_pic_link)
    book_credentials.append(author)

    return book_credentials


def get_comments(soup):

    comments = soup.select('span.black')
    all_comments = [comment.text for comment in comments]

    return all_comments

def get_genres(soup):

    genres = soup.select('span.d_book a')
    return [genre.text for genre in genres]


def download_txt(url, filename, folder='books/'):

    book_page = requests.get(url, allow_redirects=False)
    book_page.raise_for_status()
    check_for_redirect(book_page)
    filename = sanitize_filename(filename)

    with open(f"{os.path.join(folder, filename)}", 'wb') as file:
        file.write(book_page.content)


def download_book_cover(filename, book_cover_url, folder='images/'):

    book_cover = requests.get(book_cover_url, allow_redirects=False)
    book_cover.raise_for_status()
    check_for_redirect(book_cover)
    filename = sanitize_filename(filename)

    with open(f"{os.path.join(folder, filename)}.jpg", 'wb') as file:
        file.write(book_cover.content)


def main():

    parser = argparse.ArgumentParser(description="The script downloads books from 'tululu.org' portal")
    parser.add_argument('-s', '--start_page', default=0, help="Starting page", type=int)
    parser.add_argument('-e', '--end_page', default=700, help="Ending page", type=int)
    parser.add_argument('--skip_imgs', default=False, help="Turn off images download", type=bool)
    parser.add_argument('--skip_txt', default=False, help="Turn off texts download", type=bool)
    parser.add_argument('--dest_folder', default='', help="Destination folder path", type=str)
    parser.add_argument('--json_path', default='', help="JSON folder path", type=str)
    args = parser.parse_args()

    start_page = args.start_page
    end_page = args.end_page + 1
    dest_folder = args.dest_folder
    json_path = args.json_path
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt

    if dest_folder:
        os.chdir(dest_folder)

    folders = ['books', 'images']

    if json_path:
        folders.append(json_path)

    for folder in folders:

        parent_dir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(parent_dir, folder)

        try:
            os.makedirs(path, exist_ok = True)
            print("Folder '%s' created successfully" %folder)
        except OSError as error:
            print("Folder '%s' can not be created")

    books_info_all = []

    for page in range (start_page, end_page):

        if not page:
            url = f'https://tululu.org/l55'
        else:
            url = f'https://tululu.org/l55/{page}'

        try:
            book_page = requests.get(url)
            book_page.raise_for_status()
            soup = BeautifulSoup(book_page.text, 'lxml')
            books_links = soup.select('.bookimage a')

            for link in books_links:

                book_link = urljoin(url, link.get('href'))
                book_soup = make_soup(book_link)
                url, title, book_cover_url, author = get_book_link_credentials(book_soup, book_link)
                comments = get_comments(book_soup)
                genres = get_genres(book_soup)

                if not skip_txt:
                    download_txt(url, f'{n}_{title}')
                if not skip_imgs:
                    download_book_cover(f'{n}_{title}', book_cover_url)

                books_info = {
                    'title': title,
                    'author': author,
                    'img_source': book_cover_url,
                    'book_path': url,
                    'comments': comments,
                    'genres': genres,
                }

                books_info_all.append(books_info)

                with open(f"{os.path.join(json_path, 'books_about')}", 'w', encoding='utf8') as json_file:
                    json.dump(books_info_all, json_file, ensure_ascii=False)

        except requests.exceptions.ConnectionError:
            logging.exception('Connection issues, will retry after timeout.')
            print('Connection issues, will retry after timeout.')
            time.sleep(60)
        except requests.exceptions.HTTPError:
            print('HTTP Error, broken link or redirect')
        except TypeError:
            print(f'Unable to make soup for book {n} due to insufficient data')
        except IndexError:
            print(f'Unable to download book {n} due to missing link')


if __name__ == '__main__':
    main()