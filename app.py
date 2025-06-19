import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# === Google Drive file download ===
def download_file_from_drive(url, output):
    file_id = url.split("/d/")[1].split("/")[0]
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# === Ensure files are downloaded ===
if not os.path.exists("movies_dict.pkl"):
    download_file_from_drive("https://drive.google.com/file/d/1PKEYeOlEhuI2q5HP08VrwwXAEnL99WQC/view?usp=drive_link", "movies_dict.pkl")

if not os.path.exists("similarity.pkl"):
    download_file_from_drive("https://drive.google.com/file/d/1zUhTtkLmBMXqYa7voDBdu-KP0UBE4FXf/view?usp=drive_link", "similarity.pkl")

# === Load data ===
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# === Fetch poster from TMDb ===
def fetch_poster(movie_id):
    api_key = 'YOUR_TMDB_API_KEY'  # Replace with your actual TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# === Recommendation logic ===
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# === Streamlit UI ===
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Choose a movie to get recommendations", movies["title"].values)

if st.button("Recommend"):
    try:
        names, posters = recommend(selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
    except Exception as e:
        st.error("⚠️ Error during recommendation. Please try again or check TMDb API key.")
        st.code(str(e), language="text")
