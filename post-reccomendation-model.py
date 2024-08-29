import pandas as pd
import json
import SqlServerManager as sql
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import  GridSearchCV
from surprise import Reader
from itertools import groupby
from operator import itemgetter

dbReader = sql.DatabaseReader(".", # sql Server instance 
                              "post-reccomendation-model", # database name
                              "sa", # database user 
                              "admin" # database bassword
                              )

post_data = pd.read_json(json.dumps(dbReader.GetIntrestsWithPosts()))
rateLimits = dbReader.GetRateingLimits()

dataframe = pd.DataFrame(post_data)
combine_post_rating = post_data.dropna(axis = 0, subset = ['title'])

features = ['userid','postid', 'intrest']
reader = Reader(rating_scale=(rateLimits['minintrest'], rateLimits['maxintrest']))
data = Dataset.load_from_df(combine_post_rating[features], reader)
param_grid = {'n_epochs': [5,300], 'lr_all': [0.002, 0.005],
              'reg_all': [0.4, 0.6]}

gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)
model_svd = gs.best_estimator['rmse']
model_svd.fit(data.build_full_trainset())


def get_recommendations(user_id, model, post_ids, n_recommendations=10):
    predictions = []
    for post_id in post_ids:

        prediction = model.predict(user_id, post_id['postid'])
        predictions.append((post_id, prediction.est))


    grouped_predictions = {k: list(v) for k, v in groupby(predictions, key=lambda x: x[0]['postid'])}

    highest_in_group = []
    for group_key, group in grouped_predictions.items():
        highest_item = max(group, key=lambda x: x[1])
        user_ids = [item[0]['userid'] for item in group]
        highest_item[0]['userids'] = user_ids       
        highest_in_group.append(highest_item)
    
    highest_in_group.sort(key=lambda x: x[1], reverse=True)
    top_n_predictions = highest_in_group[:n_recommendations]
    
    print(f"Top {n_recommendations} recommendations for user {user_id}:")
    for i, (post_id, est_score) in enumerate(top_n_predictions, 1):
        print(f"{i}. {post_id['title']} (Predicted Interest Score: {est_score:.2f}) \n  \t *Post#: {post_id['postid']} \n \t *Category: {post_id['category']} \n \t *Recommended based on user# {post_id['userids']} \n")
        
    return top_n_predictions



user_id = '55' # userId
potentialPosts = dbReader.GetPostsNotViewedByUser(user_id)
result =get_recommendations(user_id, model_svd, potentialPosts, n_recommendations=10)# The Result object Containing  all the needed data