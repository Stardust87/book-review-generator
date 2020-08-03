from keyword_encode import encode_keywords
import ray
import pandas as pd

# def replace_non_ascii_chars(text):
#     text = text.replace(chr(8216), '\'')
#     text = text.replace(chr(8217), '\'')
#     text = text.replace(chr(8220), '\"')
#     return text

# def is_non_ascii(text):
#     for char in text:
#         if ord(char) >= 128:
#             # print(char, ord(char))
#             return True
    
#     return False

# def remove_non_ascii_reviews(df):
#     new_reviews = []

#     for review in df.iterrows():
#         review[1]['user_review'] = replace_non_ascii_chars(review[1]['user_review'])
#         if not is_non_ascii(review[1]['user_review']):
#             new_reviews.append(review[1].values)
    
#     new_df = pd.DataFrame(new_reviews, columns=df.columns)
#     return new_df

if __name__ == "__main__":
    df = pd.read_csv('./data/reviews_test.csv')
    # df = remove_non_ascii_reviews(df)
    # df.to_csv('./data/reviews_test_no_ascii.csv', index=False, encoding='ascii')

    ray.init(object_store_memory=100 * 1000000,
            redis_max_memory=100 * 1000000)

    encode_keywords(csv_path='./data/preprocessed/reviews_nlp.csv',
                    out_path='./data/reviews_test_encoded.txt',
                    category_field='category',
                    title_field='user_review',
                    keyword_gen='user_review')    

    # with open('./data/reviews_test_no_ascii.csv', encoding='ascii') as f:
    #     for char in f.read():
    #         print(char)
    #         if ord(char) >= 128:
    #             print(char, ord(char))
