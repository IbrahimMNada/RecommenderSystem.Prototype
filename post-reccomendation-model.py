import pandas as pd
import numpy as np
import json

from sklearn.model_selection import train_test_split
import SqlServerManager as sql
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import  GridSearchCV
from surprise import Reader

dbReader = sql.DatabaseReader(".", # sql Server instance 
                              "post-reccomendation-model", # database name
                              "sa", # database user 
                              "P@ssw0rd" # database bassword
                              )


post_data = pd.read_json(json.dumps(dbReader.GetAllPosts()))
user_data = pd.read_json(json.dumps(dbReader.GetAllUsers()))
view_data = pd.read_json(json.dumps(dbReader.GetAllPostViews()))


dataframe = pd.DataFrame(view_data)
df = pd.merge(dataframe, post_data ,on='post_id')

combine_post_rating = df.dropna(axis = 0, subset = ['title'])
rating_popular_post = combine_post_rating.drop_duplicates(['user_id', 'post_id'])
max_rating = np.amax( view_data['intrest'] )
min_rating = np.amin( view_data['intrest'] )


features = ['user_id','post_id', 'intrest']
reader = Reader(rating_scale=(min_rating, max_rating))
data = Dataset.load_from_df(rating_popular_post[features], reader)
param_grid = {'n_epochs': [5, 40], 'lr_all': [0.002, 0.005],
              'reg_all': [0.4, 0.6]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)


model_svd = gs.best_estimator['rmse']
model_svd.fit(data.build_full_trainset())

def get_recommendations(user_id, model, post_ids, post_titles, n_recommendations=10):

    user_posts = set(rating_popular_post[rating_popular_post['user_id'] == user_id]['post_id'].tolist())


    all_posts = set(post_ids)
    posts_to_predict = all_posts - user_posts

    predictions = []
    for post_id in posts_to_predict:

        prediction = model.predict(user_id, post_id)
        predictions.append((post_id, prediction.est))


    predictions.sort(key=lambda x: x[1], reverse=True)


    top_n_predictions = predictions[:n_recommendations]

    print(f"Top {n_recommendations} recommendations for user {user_id}:")
    for i, (post_id, est_score) in enumerate(top_n_predictions, 1):
        post_title = post_titles[post_titles['post_id'] == post_id]['title'].values[0]
        print(f"{i}. {post_title} (Predicted Interest Score: {est_score:.2f})  post_id: {post_id}   - Category: {dbReader.GetPostCategory(post_id)}")


all_post_ids = rating_popular_post['post_id'].unique()


post_titles = post_data[['post_id', 'title']]


user_id = '5eece14ffc13ae660911112c' # userId
get_recommendations(user_id, model_svd, all_post_ids, post_titles, n_recommendations=10)

