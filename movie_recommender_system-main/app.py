import requests
import streamlit as st
import pickle
import pandas as pd
from requests import api


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4d789beb3eb00386542e6e48a4daeeb3&language=en-US'.format(movie_id))
    data = response.json()
    #st.text(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'How would like to be contacted?',
    (movies['title'].values)
)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    num_columns = 5  # Number of columns to display the recommendations
    num_recommendations = len(names)
    num_per_column = num_recommendations // num_columns
    remainder = num_recommendations % num_columns

    # Distribute the recommendations evenly across columns
    columns = st.columns(num_columns)
    for i in range(num_columns):
        with columns[i]:
            start_index = i * num_per_column
            end_index = start_index + num_per_column
            if i < remainder:
                end_index += 1
            for j in range(start_index, end_index):
                st.write(names[j])
                st.image(posters[j])
