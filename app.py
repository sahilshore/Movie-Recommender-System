import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(
            "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id),
            timeout=5
        )
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

def Recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

Salected_Movie_Name = st.selectbox(
    'How would you like to be contacted',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = Recommend(Salected_Movie_Name)

    col0, col1, col2, col3, col4 = st.columns(5)  # changed from st.beta_columns
    with col0:
        st.text(names[0])
        st.image(posters[0])
    with col1:
        st.text(names[1])
        st.image(posters[1])
    with col2:
        st.text(names[2])
        st.image(posters[2])
    with col3:
        st.text(names[3])
        st.image(posters[3])
    with col4:
        st.text(names[4])
        st.image(posters[4])
