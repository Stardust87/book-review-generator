from connect import connect_db

class FireAPI:
    def __init__(self, path_to_key):
        self.db = connect_db(path_to_key)

    def get_book_by_id(self, book_id):
        book_ref = self.db.collection(u'books').document(book_id)
        book = book_ref.get()
        if book.exists:
            return book.to_dict()
        else:
            raise ValueError(f'There is no book with id {book_id}.')
    
    def get_book_reviews_by_id(self, book_id):
        book_ref = self.db.collection(u'books').document(book_id)
        if not book_ref.get().exists:
            raise ValueError(f'There is no book with id {book_id}.')

        reviews = book_ref.collection(u'reviews').stream()
        return [ review.to_dict() for review in reviews ]
    
    def add_book(self, book_id, book_obj):
        book_ref = self.db.collection(u'books').document(book_id)
        if book_ref.get().exists:
            print(f"Warning: The book with id {book_id} has already been added.")
        else:  
            self.db.collection(u'books').document(book_id).set(book_obj)

    def add_review(self, book_id, review_obj):
        # TODO: do not check if review is repeated
        reviews_ref = self.db.collection(u'books').document(book_id).collection(u'reviews')
        is_repeated = reviews_ref.where('user_id', '==', review_obj['user_id']).get()
        if not is_repeated:
            self.db.collection(u'books').document(book_id).collection('reviews').add(review_obj)
        else:
            print(f"Warning: The book with id {book_id} already has the review given by user {review_obj['user_id']}.")

if __name__ == "__main__":
    api = FireAPI("./database/private_key.json")
    print(api.get_book_reviews_by_id(u"1"))