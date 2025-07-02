import streamlit as st
import pandas as pd
import requests  #to get the poster image from the API
import pickle

with open('movies.pkl', 'rb') as f:
    movies, cosine_sim = pickle.load(f)
    
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0] # getting the index of the movie
    sim_scores = list(enumerate(cosine_sim[idx])) # getting the similarity scores for that movie
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) # sorting the scores in descending order
    sim_scores = sim_scores[1:11] # getting the top 10 similar movies (excluding itself)
    movie_indices = [i[0] for i in sim_scores] # extracting the indices of the similar movies
    return movies['title'].iloc[movie_indices] # returning the titles of the similar movies


def get_poster(movie_id):
    api_key = '8d04eff98c022851f098c1c51f88eb9f'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f'https://image.tmdb.org/t/p/w500{poster_path}'
    return full_path


st.title('Movie Recommendation System')
st.subheader('Get recommendations based on your favorite movie!')

selected_movie = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Get Recommendations'):
    recommendations = get_recommendations(selected_movie)
    st.write('Recommended Movies:')
    
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]#['title']
                movie_id = movies[movies['title'] == movie_title].iloc[0]['movie_id'] #recommendations.iloc[j]['movie_id']
                poster_url = get_poster(movie_id)
                with col:
                    st.image(poster_url, width=150)
                    st.write(movie_title)
                    

                    
#python -m streamlit run app.py
