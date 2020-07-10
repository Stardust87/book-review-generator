import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def connect_db(path_to_key):
    cred = credentials.Certificate(path_to_key)
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

if __name__ == "__main__":
    db = connect_db("./database/private_key.json")

    books_ref = db.collection(u'books')
    docs = books_ref.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
        reviews_ref = books_ref.document(doc.id).collection(u'reviews')
        reviews = reviews_ref.stream()
        for review in reviews:
            print(f'{review.id} => {review.to_dict()}')