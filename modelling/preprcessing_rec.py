import time, csv
import pandas as pd
import numpy as np

from config import preprocessing_cfg_rec as cfg

def preprocess_rec(books_df, reviews_df):
    # keep only book type media
    books_df = books_df.loc[books_df.media_type == 'book']

    # keep only english books
    english_codes = cfg['languages']
    books_df = books_df.loc[books_df.language.isin(english_codes)]

    # link other books editions to its best_id
    best_edition_books = books_df.loc[books_df.id == books_df.best_id]
    not_best_edition_books = books_df.loc[books_df.id != books_df.best_id]
    missing_books = []

    for row in not_best_edition_books.iterrows():
        best_book_id = row[1]['best_id']
        book_id = row[1]['id']
        
        if best_book_id in best_edition_books.id:
            reviews_df.loc[reviews_df.book_id == book_id, 'book_id'] = best_book_id
        else:
            book = not_best_edition_books.loc[not_best_edition_books.id == book_id, :]
            best_edition_books.append(book)
            missing_books.append(best_book_id)

    books_df = best_edition_books

    # remove books with less than X reviews
    min_reviews_per_book = cfg['min_reviews_per_book']
    reviews_per_book = reviews_df.groupby('book_id').count().user_id
    books = reviews_per_book.loc[reviews_per_book >= min_reviews_per_book].index.to_list()
    books_df = books_df.loc[books_df.id.isin(books)]


    ### AFTER PROCESSING BOOKS, REMOVE REDUNDANT ONES FROM REVIEWS_DF
    redundant_books = ~reviews_df.book_id.isin(books_df.id)
    reviews_df = reviews_df.drop(reviews_df[redundant_books].index)

    # get users with min number of reviews
    min_reviews_per_user = cfg['min_reviews_per_user']
    reviews_per_user = reviews_df.groupby(['user_id']).count().book_id
    users = reviews_per_user.loc[reviews_per_user > min_reviews_per_user].index.to_list()
    reviews_df = reviews_df.loc[reviews_df.user_id.isin(users)]

    return books_df, reviews_df, missing_books

if __name__ == "__main__":
    reviews_df = pd.read_csv('./data/reviews.csv')
    books_df = pd.read_csv('./data/books.csv')

    start = time.perf_counter()
    books_df, reviews_df, missing_books = preprocess_rec(books_df, reviews_df)
    end = time.perf_counter()
    print(f'Data has been processed in {(end-start):.2f} seconds.')

    books_df.to_csv('./data/preprocessed/books.csv', index=False)
    reviews_df.to_csv('./data/preprocessed/reviews.csv', index=False)
    reviews_df.user_review.to_csv('./data/preprocessed/text_reviews_rec.csv', index=False, header=False, quoting=csv.QUOTE_NONE, escapechar = ' ')

