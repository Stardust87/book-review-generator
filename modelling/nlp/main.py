from keyword_encode import encode_keywords
import ray
import pandas as pd

input_path = './data/preprocessed/reviews_nlp.csv'
output_path = './data/preprocessed/reviews_balanced.csv'
output_encoded_path = './data/reviews_nlp_encoded.txt'

reviews_df = pd.read_csv('./data/preprocessed/reviews_nlp.csv')

# balance positive to negative sample ratio
neg_reviews_df = reviews_df.loc[reviews_df.rating_category == 'negative']
pos_reviews_df = reviews_df.loc[reviews_df.rating_category == 'positive']

negative_reviews_count = reviews_df.groupby('rating_category').count().loc['negative','book_id']
pos_reviews_df = pos_reviews_df.sample(n=negative_reviews_count, random_state=42)

final_df = pd.concat([pos_reviews_df, neg_reviews_df]).sample(frac=1).reset_index(drop=True)
final_df.to_csv(output_path, index=False)

ray.init(object_store_memory=100 * 1000000,
        redis_max_memory=100 * 1000000)

# create encoded dataset, ready to train
encode_keywords(csv_path=output_path,
                out_path=output_encoded_path,
                category_field='rating_category',
                title_field='user_review',
                keyword_gen='user_review')    

