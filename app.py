import os
import gdown
import pickle
import pandas as pd
import streamlit as st
import requests

# Google Drive File IDs
MOVIES_FILE_ID = "1zUhTtkLmBMXqYa7voDBdu-KP0UBE4FXf"
SIMILARITY_FILE_ID = "1PKEYeOlEhuI2q5HP08VrwwXAEnL99WQC"

# Download from Google Drive if not already present
if not os.path.exists("movies_dict.pkl"):
    gdown.download(f"https://drive.google.com/uc?id={MOVIES_FILE_ID}", "movies_dict.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}", "similarity.pkl", quiet=False)

# Load data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US", timeout=10)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def Recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = Recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
