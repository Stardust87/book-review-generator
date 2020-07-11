import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def connect_db(path_to_key):
    cred = credentials.Certificate(path_to_key)
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db