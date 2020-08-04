import time, csv
import pandas as pd
import numpy as np

from config import preprocessing_cfg_nlp as cfg

def is_non_ascii(text):
    for char in text:
        if ord(char) >= 128:
            return True

    return False

def preprocess_nlp(books_df, reviews_df):
    # keep only book type media
    books_df = books_df.loc[books_df.media_type == 'book']

    # keep only english books
    english_codes = cfg['languages']
    books_df = books_df.loc[books_df.language.isin(english_codes)]

    # remove books with less than X reviews
    min_reviews_per_book = cfg['min_reviews_per_book']
    reviews_per_book = reviews_df.groupby('book_id').count().user_id
    books = reviews_per_book.loc[reviews_per_book >= min_reviews_per_book].index.to_list()
    books_df = books_df.loc[books_df.id.isin(books)]

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

    # remove entries with text reviews shorter than X chars
    reviews_df.user_review = reviews_df.user_review.replace("None", "")
    reviews_df['review_length'] = reviews_df.user_review.apply(len)
    min_length_of_text_review = cfg['min_length_of_text_review']
    reviews_df = reviews_df.loc[reviews_df.review_length >= min_length_of_text_review]

    # remove books with less than X text reviews
    min_text_reviews_per_book = cfg['min_text_reviews_per_book']
    text_reviews_per_book = reviews_df.groupby('book_id').count().user_review
    books = text_reviews_per_book.loc[text_reviews_per_book >= min_text_reviews_per_book].index.to_list()
    books_df = books_df.loc[books_df.id.isin(books)]

    ### AFTER PROCESSING BOOKS, REMOVE REDUNDANT ONES FROM REVIEWS_DF
    redundant_books = ~reviews_df.book_id.isin(books_df.id)
    reviews_df = reviews_df.drop(reviews_df[redundant_books].index)

    # replace a few non ascii chars and keep only reviews with all ascii chars
    new_reviews = []
    for review in reviews_df.iterrows():
        # TODO: handle ALL non-ascii chars present in data
        review[1]['user_review'] = review[1]['user_review'].replace(chr(8216), '\'').replace(chr(8217), '\'').replace(chr(8220), '\"')
        if not is_non_ascii(review[1]['user_review']):
            new_reviews.append(review[1].values)
    reviews_df = pd.DataFrame(new_reviews, columns=reviews_df.columns)

    return books_df, reviews_df, missing_books

if __name__ == "__main__":
    reviews_df = pd.read_csv('./data/reviews.csv')
    books_df = pd.read_csv('./data/books.csv')

    start = time.perf_counter()
    books_df, reviews_df, missing_books = preprocess_nlp(books_df, reviews_df)
    end = time.perf_counter()
    print(f'Data has been processed in {(end-start):.2f} seconds.')

    books_df.to_csv('./data/preprocessed/books_nlp.csv', index=False)
    reviews_df.to_csv('./data/preprocessed/reviews_nlp.csv', index=False)
    reviews_df.user_review.to_csv('./data/preprocessed/text_reviews.csv', index=False, header=False, quoting=csv.QUOTE_NONE, escapechar = ' ')

