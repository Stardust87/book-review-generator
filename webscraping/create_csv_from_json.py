import json, glob
import numpy as np
import pandas as pd

from progress.bar import Bar

def add_book(book_review, book_dict):
    book_id = int(book_review['book_id'])
    if book_id in book_dict['book_id']:
        return book_dict

    book_dict['book_id'].append(book_id)
    book_dict['book_title'].append(book_review['book_title'])
    book_dict['book_author'].append(book_review['book_author'])
    book_dict['book_avg_rating'].append(book_review['book_avg_rating'])
    return book_dict

def add_review(book_review, review_dict, user_id):
    review_dict['book_id'].append(int(book_review['book_id']))
    review_dict['user_id'].append(user_id)
    review_dict['user_rating'].append(book_review['user_rating'])
    review_dict['user_review'].append(book_review['user_review'])
    return review_dict

def add_user(filename, book_dict, review_dict):
    with open(filename) as json_file:
        data = json.load(json_file)

    if len(data) <= 1:
        return book_dict, review_dict

    user_id = int(filename.split('_')[-1].split('.')[0])

    for book_review in data:
        book_dict = add_book(book_review, book_dict)
        review_dict = add_review(book_review, review_dict, user_id)
    
    return book_dict, review_dict

def create_csv(users_path, target_path):
    books_dict = {
        'book_id': [],
        'book_title': [],
        'book_author': [],
        'book_avg_rating': []
    }
    reviews_dict = {
        'book_id': [],
        'user_id': [],
        'user_rating': [],
        'user_review': []
    }

    filenames = glob.glob(users_path+'*')
    bar = Bar('Processing', max=len(filenames))
    for filename in filenames:
        books_dict, reviews_dict = add_user(filename, books_dict, reviews_dict)
        bar.next()
    bar.finish()

    books_df = pd.DataFrame.from_dict(books_dict)
    reviews_df = pd.DataFrame.from_dict(reviews_dict)

    books_df.to_csv(target_path+'books_short.csv', index=False)
    reviews_df.to_csv(target_path+'reviews.csv', index=False)


if __name__ == "__main__":
    PATH = '.\\data\\users\\'
    TARGET = '.\\data\\'
    create_csv(PATH, TARGET)