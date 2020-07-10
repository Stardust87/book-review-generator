import glob
import json
import shutil

from api import FireAPI

def parse_review_entry(book_review, user_id):
    book_id = str(book_review['book_id'])

    if book_review['user_rating'] == -1 and book_review['user_review'] == "None":
        return None

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
        parsed = parse_review_entry(book_review, user_id)
        if not parsed:
            continue
        else:
            book, review = parsed
            user_reviews.append((book, review))

    return user_reviews

def upload_user(api, filename):
    user_data = read_user(filename)

    if len(user_data) > 1:
        # for book_obj, review_obj in user_data:
        #     api.add_book(*book_obj)
        #     api.add_review(book_obj[0], review_obj)
        
        destination = filename.split('\\users')
        destination.insert(1, '\\uploaded_users')

        shutil.move(filename, ''.join(destination))
    else: 
        user_id = filename.split('\\')[-1]
        print(f"User {user_id} has less than or equal to 1 valid reviews, it's worthless.")
        destination = filename.split('\\users')
        destination.insert(1, '\\worthless_users')

        shutil.move(filename, ''.join(destination))


def upload_downloaded_users(users_path, key):
    api = FireAPI(KEY_PATH)

    user_paths = glob.glob(USER_PATH+'*')
    for key, path in enumerate(user_paths):
        upload_user(api, path)
        print(f'Finished uploading user {key+1}/{len(user_paths)}')

if __name__ == "__main__":
    USER_PATH = '.\\data\\users\\'
    KEY_PATH = '.\\database\\private_key.json'

    upload_downloaded_users(USER_PATH, KEY_PATH)

