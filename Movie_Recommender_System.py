import streamlit as st
import streamlit.components.v1 as components
import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=96e5b3d401d0167bed258681431d60b1&language=en-US".format(
        movie_id
    )
    data = requests.get(url)
    data = data.json()
    poster_path = data["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154),
]

movies = pickle.load(
    open(
        "movie_list.pkl",
        "rb",
    )
)
similar = pickle.load(
    open(
        "similarity.pkl",
        "rb",
    )
)
movies_list = movies["title"].values

st.header("Movie Recommender System")

imageCarouselComponent = components.declare_component(
    "image-carousel-component", path="frontend/public"
)
imageCarouselComponent(imageUrls=imageUrls, height=200)

select_value = st.selectbox("Select Movie", movies_list)


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distance = sorted(
        list(enumerate(similar[index])), reverse=True, key=lambda vector: vector[1]
    )
    recommend_movies = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movies, recommend_poster


if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(select_value)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
    # with col6:
    #     st.text(movie_name[5])
    #     st.image(movie_poster[5])
    # with col7:
    #     st.text(movie_name[6])
    #     st.image(movie_poster[6])
    # with col8:
    #     st.text(movie_name[7])
    #     st.image(movie_poster[7])
