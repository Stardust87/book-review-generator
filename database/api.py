from connect import connect_db

class FireAPI:
    def __init__(self, path_to_key):
        self.db = connect_db(path_to_key)

    def get_book_by_id(self, book_id):
        book_ref = self.db.collection(u'books').document(book_id)
        book = book_ref.get().to_dict()
        if not book:
            raise ValueError(f'There is no book with id {book_id}.')
        else:
            return book_ref.get().to_dict()
    
    def get_book_reviews_by_id(self, book_id):
        book_ref = self.db.collection(u'books').document(book_id)
        if not book_ref.get().to_dict():
            raise ValueError(f'There is no book with id {book_id}.')

        reviews = book_ref.collection(u'reviews').stream()
        return [ review.to_dict() for review in reviews ]

if __name__ == "__main__":
    api = FireAPI("./database/private_key.json")
    print(api.get_book_reviews_by_id(u"66559"))