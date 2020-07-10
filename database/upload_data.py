import glob
import json

from api import FireAPI

def parse_review_entry(book_review, user_id):
    book_id = str(book_review['book_id'])

    book = {
        u'author': book_review['book_author'],
        u'avg_rating': book_review['book_avg_rating'],
        u'title': book_review['book_title']
    }

    review = {
        u'rating': book_review['user_rating'],
        u'review': book_review['user_review'],
        u'user_id': user_id
    }

    return (book_id, book), review

def read_user(filename):
    with open(filename) as json_file:
        data = json.load(json_file)

    user_id = filename.split('_')[-1].split('.')[0]
    user_reviews = []

    for book_review in data:
        book, review = parse_review_entry(book_review, user_id)
        user_reviews.append((book, review))

    return user_reviews

def upload_user(api, filename):
    user_data = read_user(filename)

    for book_obj, review_obj in user_data:
        api.add_book(*book_obj)
        api.add_review(book_obj[0], review_obj)


if __name__ == "__main__":
    USER_PATH = '.\\data\\users\\'
    KEY_PATH = '.\\database\\private_key.json'

    api = FireAPI(KEY_PATH)

    user_paths = glob.glob(USER_PATH+'*')
    for key, path in enumerate(user_paths):
        upload_user(api, path)
        print(f'Finished uploading user {key+1}/{len(user_paths)}')

    #TODO: get uploaded users so it does not have to upload same users