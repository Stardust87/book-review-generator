import random

import numpy as np
import pandas as pd

from preprocessing import preprocess

def train_test_split(df, split_ratio):
    users = df.user_id.unique()
    train_dict = { col: [] for col in df.columns.to_list() }
    test_dict = { col: [] for col in df.columns.to_list() }
    users_books = df.groupby('user_id').book_id.apply(list).to_dict()
    users_ratings = df.groupby('user_id').user_rating.apply(list).to_dict()

    for user, books in users_books.items():

        max_index = len(books)-1
        test_indices = random.sample(range(max_index+1), int(np.ceil(split_ratio*max_index)))
        train_indices = list(set(range(max_index+1))-set(list(test_indices)))

        test_books = np.array(books)[test_indices]
        train_books = np.array(books)[train_indices]

        ratings = np.array(users_ratings[user])
        test_ratings = ratings[test_indices]
        train_ratings = ratings[train_indices]

        test_dict['user_id'] += [user]*len(test_indices)
        test_dict['book_id'] += list(test_books)
        test_dict['user_rating'] += list(test_ratings)
        
        train_dict['user_id'] += [user]*len(train_indices)
        train_dict['book_id'] += list(train_books)
        train_dict['user_rating'] += list(train_ratings)

    test_df = pd.DataFrame.from_dict(test_dict)
    train_df = pd.DataFrame.from_dict(train_dict)

    all_train_books = train_df.book_id.unique()
    all_test_books = test_df.book_id.unique()
    unique_for_train_set = set(all_train_books)-set(all_test_books)
    unique_for_test_set = set(all_test_books)-set(all_train_books)
    
    for book_id in list(unique_for_train_set):
        train_df, test_df = move_sample_book_review(book_id, train_df, test_df)

    for book_id in list(unique_for_test_set):
        test_df, train_df = move_sample_book_review(book_id, test_df, train_df)

    return train_df, test_df

def move_sample_book_review(book_id, df1, df2):
    # IDEA: maybe move more books depending on difference between sets?
    row_indices = df1.loc[df1.book_id == book_id].index.to_list()
    if row_indices:
        selected_index = random.choice(row_indices)
        row_to_move = df1.loc[selected_index, :]
        df1 = df1.drop([selected_index])
        df2 = df2.append(row_to_move)

    return df1, df2

def get_implicit_data(df):
    df['label'] = 1
    df.loc[df['user_rating'].isin([1, 2]), 'label'] = 0
    df = df.drop(['user_rating'], axis=1)
    return df


if __name__ == "__main__":

    reviews_df = pd.read_csv('./data/reviews.csv')
    books_df = pd.read_csv('./data/books.csv')

    books_df, reviews_df, missing_books = preprocess(books_df, reviews_df)

    reviews_df = reviews_df.reindex(columns=['user_id', 'book_id', 'user_rating'])
    train_df, test_df = train_test_split(reviews_df, 0.25)
    train_df = get_implicit_data(train_df)
    test_df = get_implicit_data(test_df)
