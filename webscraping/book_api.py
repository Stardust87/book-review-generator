import requests, time, glob
import pandas as pd

from api_key import API_KEY, SECRET

def get_books_to_download(path_to_books_list, downloaded_path=None):
    reviews_df = pd.read_csv(path_to_books_list)
    all_books = reviews_df.groupby('book_id').count().sort_values(by='user_id', ascending=False).index.to_list()

    if downloaded_path:
        downloaded = get_downloaded_books_ids(downloaded_path)
        left_to_download_books = [ book for book in all_books if not book in downloaded ]
        return left_to_download_books
    else:
        return all_books

def get_downloaded_books_ids(path):
    filenames = glob.glob(path+'*')
    books_ids = [ int(f.split('_')[-1].split('.')[0]) for f in filenames ]
    return books_ids

def download_book(book_id):
    URL = f'https://www.goodreads.com/book/show/{book_id}.xml?key={API_KEY}'
    res = requests.get(URL)
    if res.status_code == 200:
        print(f'{book_id} -> {res.status_code}')
        return res.text
    else:
        return 0

def save_xml(data, filename):
    with open(filename, 'w+', encoding="utf-8") as file_xml:
        file_xml.write(data)

def download_batch_of_books(num_of_books):
    DOWNLOADED_BOOKS_PATH = './data/books_xml/'
    BOOKS_CSV_PATH = './data/reviews.csv'

    books_to_download = get_books_to_download(BOOKS_CSV_PATH, DOWNLOADED_BOOKS_PATH)
    books_batch = books_to_download[:num_of_books]

    for book_id in books_batch:
        try:
            book_data = download_book(book_id)
            if book_data:
                save_xml(book_data, f'./data/books_xml/book_{book_id}.xml')
        except:
            print(f"Error while downloading book {book_id}..")
        finally:
            time.sleep(1.5)



if __name__ == "__main__":
    download_batch_of_books(5)

