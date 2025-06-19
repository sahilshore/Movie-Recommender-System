import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Page config and title
st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommender System")
st.write("Loading models... please wait")

# Download and cache models from Google Drive
@st.cache_data
def download_movies_dict():
    url = 'https://drive.google.com/uc?id=1zUhTtkLmBMXqYa7voDBdu-KP0UBE4FXf'
    output = 'movies_dict.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return output

@st.cache_data
def download_similarity():
    url = 'https://drive.google.com/uc?id=1PKEYeOlEhuI2q5HP08VrwwXAEnL99WQC'
    output = 'similarity.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return output

# Load models
download_movies_dict()
download_similarity()
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# UI input and output
selected_movie_name = st.selectbox("Select a movie to get recommendations", movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
