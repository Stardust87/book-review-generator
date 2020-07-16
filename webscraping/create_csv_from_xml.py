import glob, json
import numpy as np
import pandas as pd

from xml.dom import minidom
from pathlib import Path
from progress.bar import Bar

def should_filter_out_shelf(shelf_name):
    if 'read' in shelf_name:
        return True

def add_book(filename, books_dict):
    with open(filename, encoding='latin-1') as file_xml:
        xml_data = file_xml.read()

    book_xml = minidom.parseString(xml_data)
    book = book_xml.getElementsByTagName('book')[0]
    book_work = book.getElementsByTagName('work')[0]

    books_dict['id'].append(int(book.getElementsByTagName('id')[0].firstChild.data))
    books_dict['best_id'].append(int(book_work.getElementsByTagName('best_book_id')[0].firstChild.data))
    books_dict['title'].append(book.getElementsByTagName('title')[0].firstChild.data)
    books_dict['author'].append(book.getElementsByTagName('author')[0].getElementsByTagName('name')[0].firstChild.data)
    books_dict['description'].append(book.getElementsByTagName('description')[0].firstChild.data.replace('<br /><br />', '\n').replace('<br />', '\n'))
    books_dict['year'].append(int(book_work.getElementsByTagName('original_publication_year')[0].firstChild.data))
    books_dict['num_pages'].append(int(book.getElementsByTagName('num_pages')[0].firstChild.data))
    books_dict['format'].append(book.getElementsByTagName('format')[0].firstChild.data)
    books_dict['media_type'].append(book_work.getElementsByTagName('media_type')[0].firstChild.data)
    books_dict['language'].append(book.getElementsByTagName('language_code')[0].firstChild.data)
    books_dict['image_url'].append(book.getElementsByTagName('image_url')[0].firstChild.data)
    books_dict['average_rating'].append(float(book.getElementsByTagName('average_rating')[0].firstChild.data))
    books_dict['rating_dist'].append(book_work.getElementsByTagName('rating_dist')[0].firstChild.data)
    books_dict['ratings_count'].append(int(book_work.getElementsByTagName('ratings_count')[0].firstChild.data))
    books_dict['text_reviews_count'].append(int(book_work.getElementsByTagName('text_reviews_count')[0].firstChild.data))
    shelves = book.getElementsByTagName('shelf')
    shelves_dict = {}
    for shelf in shelves:
        shelf_name = shelf.getAttribute('name')
        if not should_filter_out_shelf(shelf_name):
            shelves_dict[shelf_name] = int(shelf.getAttribute('count'))

    books_dict['shelves'].append(json.dumps(shelves_dict))

    return books_dict

def create_csv(books_path, target_path):
    books_dict = {
        'id': [],
        'best_id': [],
        'title': [],
        'author': [],
        'description': [],
        'year': [],
        'num_pages': [],
        'format': [],
        'media_type': [],
        'language': [],
        'image_url': [],
        'average_rating': [],
        'rating_dist': [],
        'ratings_count': [],
        'text_reviews_count': [],
        'shelves': []
    }

    filenames = list(books_path.glob('*'))
    bar = Bar('Processing', max=len(filenames))
    for filename in filenames:
        books_dict = add_book(filename, books_dict)
        bar.next()
    bar.finish()

    books_df = pd.DataFrame.from_dict(books_dict)
    books_df.to_csv(target_path.joinpath('books.csv'), index=False)

if __name__ == "__main__":
    BOOKS_PATH = Path('./data/books_xml/')
    TARGET = Path('./data/')
    create_csv(BOOKS_PATH, TARGET)
    # add_book('./data/books_xml/book_890.xml')