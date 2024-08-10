import numpy  as np
import pandas as pd 
import matplotlib as plt
import seaborn as sns 
import warnings
warnings.filterwarnings('ignore')
import time



movies = pd.read_csv('/Users/rjpathak/Downloads/Movie+Assignment+Data.csv')
columns_to_drop = [
    'director_facebook_likes',
    'actor_1_facebook_likes',
    'actor_2_facebook_likes',
    'actor_3_facebook_likes',
    'actor_2_name',
    'cast_total_facebook_likes',
    'actor_3_name',
    'duration',
    'facenumber_in_poster',
    'content_rating',
    'country',
    'movie_imdb_link',
    'aspect_ratio',
    'plot_keywords',
    'color'
]
movies = movies.drop(columns= columns_to_drop)
null_percentage  = round(100 * (movies.isnull().sum() / len(movies)), 2)
columns_with_null_percentage = null_percentage[null_percentage > 5].index
movies = movies.dropna(subset= columns_with_null_percentage)
null_values = movies.isnull().sum()
columns_with_high_null_values = null_values[null_values > 5].index
movies = movies.dropna(subset= columns_with_high_null_values)
movies['language'].fillna('English', inplace= True)
movies.budget = movies.budget.apply(lambda x: x/1000000)
movies.gross = movies.gross.apply(lambda x: x/1000000)
movies['profit'] = movies['gross'] - movies['budget']
movies.drop_duplicates(inplace = True)
sorted_movies = movies.sort_values(by='profit', ascending=False)
top10 = sorted_movies.head(10)
IMDb_Top_250 = movies[movies['num_voted_users'] > 25000].sort_values(by='imdb_score', ascending=False).head(250)
IMDb_Top_250['rank'] = range(1, len(IMDb_Top_250) + 1)
Top_Foreign_Lang_Film = IMDb_Top_250[IMDb_Top_250['language'] != "English" ]
average_imdb_score = movies.groupby('director_name')['imdb_score'].mean()
top10director = average_imdb_score.sort_values(ascending=False).head(10)
movies[['genre_1', 'genre_2']] = movies['genres'].str.split('|', expand=True, n=1)
movies['genre_2'] = movies['genre_2'].str.split('|').str[0]
movies['genre_2'] = movies['genre_2'].fillna(movies['genre_1'])
PopGenre = movies.groupby(['genre_1', 'genre_2'])['gross'].mean().reset_index().sort_values(by='gross', ascending=False).head(5)
Meryl_Streep = movies[movies['actor_1_name']== "Meryl Streep"]
Leo_Caprio = movies[movies['actor_1_name']== "Leonardo DiCaprio"]
Brad_Pitt =  movies[movies['actor_1_name']== "Brad Pitt"]
Combined = pd.concat([Meryl_Streep, Leo_Caprio, Brad_Pitt], ignore_index=True)
grouped = Combined.groupby('actor_1_name')
high_mean_1 = grouped['num_critic_for_reviews'].mean()
high_mean_2 = grouped['num_user_for_reviews'].mean()


