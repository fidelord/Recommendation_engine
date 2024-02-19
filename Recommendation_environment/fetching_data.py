import pandas as pd
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

movie_soup = pd.read_csv('movie_soup.csv')
movie_soup = movie_soup.squeeze()
movie_recommendations = pd.read_csv('Movies_recommendation.csv')
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(movie_soup)
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
indices2 = pd.Series(movie_recommendations.index, index=movie_recommendations['title'])

# This is the server
def content_recommender(title, cosine_sim=cosine_sim2, df=movie_recommendations, indices=indices2):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return list(df['title'].iloc[movie_indices])


