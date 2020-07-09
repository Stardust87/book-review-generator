import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./database/private_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

books_ref = db.collection(u'books')
docs = books_ref.stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
    reviews_ref = books_ref.document(doc.id).collection(u'reviews')
    reviews = reviews_ref.stream()
    for review in reviews:
        print(f'{review.id} => {review.to_dict()}')