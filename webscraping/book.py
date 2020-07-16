import time, glob, threading
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd 
import numpy as np

from utils import save_json

def read_number(num_str):
    # example: '45,558' -> 45558
    return int(''.join(num_str.split(',')))

def download_book_data(driver, book_id):
    book_data = { 'book_id': book_id }

    driver.get("https://www.goodreads.com/book/show/"+str(book_id))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    try:
        book_data['book_title'] = soup.select('.gr-h1.gr-h1--serif')[0].text.strip()
    except:
        book_data['book_title'] = ''
    try:
        book_data['book_author'] = soup.select('.authorName')[0].text.strip()
    except:
        book_data['book_author'] = ''

    try: 
        book_data['book_avg_rating'] = float(soup.select('#bookMeta span[itemprop="ratingValue"]')[0].text.strip())
    except:
        book_data['book_avg_rating'] = -1
    try: 
        book_data['ratings_count'] = read_number(soup.select('#bookMeta a[href="#other_reviews"]')[0].text.strip().split('\n')[0])
    except:
        book_data['ratings_count'] = -1
    try: 
        book_data['reviews_count'] = read_number(soup.select('#bookMeta a[href="#other_reviews"]')[1].text.strip().split('\n')[0])
    except:
        book_data['reviews_count'] = -1

    try:
        book_data['book_description'] = soup.select("#description span")[-1].text.strip()
    except:
        book_data['book_description'] = ''
    try:
        book_data['book_format'] = soup.select("div.row span:nth-child(1)")[0].text.strip()
    except:
        book_data['book_format'] = ''
    try:
        book_data['book_language'] = soup.select("div[itemprop='inLanguage']")[0].text.strip()
    except:
        book_data['book_language'] = ''

    try:
        genre = [ value.text.strip() for value in soup.select("div.elementList  div.left") ]
        genre_users = [ read_number(value.text.strip()[:-6]) for value in soup.select("div.elementList  div.right") ]
        genre_mixed = [ (gen, users) for gen, users in zip(genre, genre_users) ]
        book_data['book_genre'] = dict(genre_mixed)
    except:
        book_data['book_genre'] = {}

    return book_data

def download_books(driver, books):
    for book_id in books:
        try:
            book_data = download_book_data(driver, int(book_id))
            if book_data['book_title']:
                save_json(book_data, f'.\\data\\books\\book_{int(book_id)}.json')
                print(f"Success: [{book_id}] {book_data['book_title']} has been downloaded")
            else:
                print(f'Error: could not download book {book_id}')
        except:
            print(f'Error: could not download book {book_id}')

def get_books_to_download(path_to_books_list, downloaded_path=None):
    books_df = pd.read_csv(path_to_books_list)
    all_books = books_df['book_id'].values

    if downloaded_path:
        downloaded = get_downloaded_books_ids(downloaded_path)
        left_to_download_books = list(set(all_books)-set(downloaded))
        return left_to_download_books
    else:
        return all_books

def get_downloaded_books_ids(path):
    filenames = glob.glob(path+'*')
    books_ids = [ int(f.split('_')[-1].split('.')[0]) for f in filenames ]
    return books_ids

def main():
    DOWNLOADED_BOOKS_PATH = '.\\data\\books\\'
    BOOKS_CSV_PATH = '.\\data\\books_short.csv'

    num_of_books_per_driver = 20
    num_of_drivers = 1
    total_num_of_books = num_of_drivers*num_of_books_per_driver

    drivers = [ webdriver.Chrome() for _ in range(num_of_drivers) ]
    # drivers = [ webdriver.Chrome(r'C:\Users\aniak\chromedriver.exe') for _ in range(num_of_drivers) ]

    books_to_download = np.array(get_books_to_download(BOOKS_CSV_PATH, DOWNLOADED_BOOKS_PATH))
    books_batch = np.split(books_to_download[:total_num_of_books], num_of_drivers)

    threads = []
    for k in range(num_of_drivers):
        t = threading.Thread(target=download_books, args=[drivers[k], books_batch[k]])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()   

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f'TASK FINISHED IN {end-start} seconds.')
    # print(download_book_data(webdriver.Chrome(), 1))