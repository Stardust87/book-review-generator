from keyword_encode import encode_keywords
import ray
import pandas as pd


df = pd.read_csv('./data/reviews_test.csv')


ray.init(object_store_memory=100 * 1000000,
        redis_max_memory=100 * 1000000)

encode_keywords(csv_path='./data/preprocessed/reviews_nlp.csv',
                out_path='./data/reviews_test_encoded.txt',
                category_field='category',
                title_field='user_review',
                keyword_gen='user_review')    


