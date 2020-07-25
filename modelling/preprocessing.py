import pandas as pd
from config import preprocessing_cfg

def preprocess(books_df, reviews_df):
    # keep only book type media
    books_df = books_df.loc[books_df.media_type == 'book']

    # keep only english books
    english_codes = preprocessing_cfg['languages']
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
            missing_books.append(best_book_id)

    books_df = best_edition_books

    ### AFTER PROCESSING BOOKS, REMOVE REDUNDANT ONES FROM REVIEWS_DF
    redundant_books = ~reviews_df.book_id.isin(books_df.id)
    reviews_df = reviews_df.drop(reviews_df[redundant_books].index)

    # get users with min number of reviews
    min_reviews_per_user = preprocessing_cfg['min_reviews_per_user']
    reviews_per_user = reviews_df.groupby(['user_id']).count().book_id
    users = reviews_per_user.loc[reviews_per_user > min_reviews_per_user].index.to_list()
    reviews_df = reviews_df.loc[reviews_df.user_id.isin(users)]

    return books_df, reviews_df, missing_books

if __name__ == "__main__":
    reviews_df = pd.read_csv('./data/reviews.csv')
    books_df = pd.read_csv('./data/books.csv')

    books_df, reviews_df, missing_books = preprocess(books_df, reviews_df)
