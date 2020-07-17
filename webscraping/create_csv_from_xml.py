import glob, json, re
import numpy as np
import pandas as pd

from xml.dom import minidom
from pathlib import Path
from progress.bar import Bar

LATIN_1_CHARS = (
    ('\xe2\x80\x99', "'"),
    ('\xc3\xa9', 'e'),
    ('\xe2\x80\x90', '-'),
    ('\xe2\x80\x91', '-'),
    ('\xe2\x80\x92', '-'),
    ('\xe2\x80\x93', '-'),
    ('\xe2\x80\x94', '-'),
    ('\xe2\x80\x94', '-'),
    ('\xe2\x80\x98', "'"),
    ('\xe2\x80\x9b', "'"),
    ('\xe2\x80\x9c', '"'),
    ('\xe2\x80\x9c', '"'),
    ('\xe2\x80\x9d', '"'),
    ('\xe2\x80\x9e', '"'),
    ('\xe2\x80\x9f', '"'),
    ('\xe2\x80\xa6', '...'),
    ('\xe2\x80\xb2', "'"),
    ('\xe2\x80\xb3', "'"),
    ('\xe2\x80\xb4', "'"),
    ('\xe2\x80\xb5', "'"),
    ('\xe2\x80\xb6', "'"),
    ('\xe2\x80\xb7', "'"),
    ('\xe2\x81\xba', "+"),
    ('\xe2\x81\xbb', "-"),
    ('\xe2\x81\xbc', "="),
    ('\xe2\x81\xbd', "("),
    ('\xe2\x81\xbe', ")")
)


def clean_latin1(data):
    try:
        return data.encode('utf-8')
    except UnicodeDecodeError:
        data = data.decode('iso-8859-1')
        for _hex, _char in LATIN_1_CHARS:
            data = data.replace(_hex, _char)
        return data.encode('utf8')

def should_filter_out_shelf(shelf_name):
    if 'read' in shelf_name:
        return True

def add_book(filename, books_dict):
    with open(filename, encoding='utf-8') as file_xml:
        xml_data = file_xml.read()

    book_xml = minidom.parseString(xml_data)
    book = book_xml.getElementsByTagName('book')[0]
    book_work = book.getElementsByTagName('work')[0]

    try:
        books_dict['id'].append(int(book.getElementsByTagName('id')[0].firstChild.data))
    except:
        books_dict['id'].append(None)

    try:
        books_dict['best_id'].append(int(book_work.getElementsByTagName('best_book_id')[0].firstChild.data))
    except:    
        books_dict['best_id'].append(None)

    try:
        books_dict['title'].append(book.getElementsByTagName('title')[0].firstChild.data)
    except:
        books_dict['title'].append(None)

    try:
        books_dict['author'].append(book.getElementsByTagName('author')[0].getElementsByTagName('name')[0].firstChild.data)
    except:
        books_dict['author'].append(None)

    try:
        description = book.getElementsByTagName('description')[0].firstChild.data.replace('<br /><br />', '\n').replace('<br />', '\n')
        description = clean_latin1(re.sub('<[^<]+?>', '', description)).decode("utf-8")
        books_dict['description'].append(description)
    except:
        books_dict['description'].append(None)

    try:
        books_dict['year'].append(int(book_work.getElementsByTagName('original_publication_year')[0].firstChild.data))
    except:
        books_dict['year'].append(None)

    try:
        books_dict['num_pages'].append(int(book.getElementsByTagName('num_pages')[0].firstChild.data))
    except:
        books_dict['num_pages'].append(None)

    try:
        books_dict['format'].append(book.getElementsByTagName('format')[0].firstChild.data)
    except:
        books_dict['format'].append(None)

    try:
        books_dict['media_type'].append(book_work.getElementsByTagName('media_type')[0].firstChild.data)
    except:
        books_dict['media_type'].append(None)

    try:
        books_dict['language'].append(book.getElementsByTagName('language_code')[0].firstChild.data)
    except:
        books_dict['language'].append(None)

    try:
        books_dict['image_url'].append(book.getElementsByTagName('image_url')[0].firstChild.data)
    except:
        books_dict['image_url'].append(None)

    try:
        books_dict['average_rating'].append(float(book.getElementsByTagName('average_rating')[0].firstChild.data))
    except:
        books_dict['average_rating'].append(None)

    try:
        books_dict['rating_dist'].append(book_work.getElementsByTagName('rating_dist')[0].firstChild.data)
    except:
        books_dict['rating_dist'].append(None)
    
    try:
        books_dict['ratings_count'].append(int(book_work.getElementsByTagName('ratings_count')[0].firstChild.data))
    except:
        books_dict['ratings_count'].append(None)
    
    try:
        books_dict['text_reviews_count'].append(int(book_work.getElementsByTagName('text_reviews_count')[0].firstChild.data))
    except:
        books_dict['text_reviews_count'].append(None)

    shelves = book.getElementsByTagName('shelf')
    shelves_dict = {}
    for shelf in shelves:
        shelf_name = shelf.getAttribute('name')
        if not should_filter_out_shelf(shelf_name):
            shelves_dict[shelf_name] = int(shelf.getAttribute('count'))

    try:
        books_dict['shelves'].append(json.dumps(shelves_dict))
    except:
        books_dict['shelves'].append(None)

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
    # add_book('./data/books_xml/book_10000191.xml', {
    #     'id': [],
    #     'best_id': [],
    #     'title': [],
    #     'author': [],
    #     'description': [],
    #     'year': [],
    #     'num_pages': [],
    #     'format': [],
    #     'media_type': [],
    #     'language': [],
    #     'image_url': [],
    #     'average_rating': [],
    #     'rating_dist': [],
    #     'ratings_count': [],
    #     'text_reviews_count': [],
    #     'shelves': []
    # })