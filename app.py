import streamlit as st
from datos import datosRecomendacion

datos = datosRecomendacion()

people = datos.get_people()
selected_person = st.selectbox(
    "Choose a person",
    people
)

genres = datos.get_genres()
selected_genre = st.selectbox(
    "Choose a genre",
    genres
)

#resetea el índice si cambia persona o género
if "last_person" not in st.session_state:
    st.session_state.last_person = selected_person

if "last_genre" not in st.session_state:
    st.session_state.last_genre = selected_genre

if (
    st.session_state.last_person != selected_person
    or
    st.session_state.last_genre != selected_genre
):

    st.session_state.song_index = 0

    st.session_state.last_person = selected_person
    st.session_state.last_genre = selected_genre

recommendations = datos.get_recommendations(
    selected_person,
    selected_genre
)

if "song_index" not in st.session_state:
    st.session_state.song_index = 0

if st.session_state.song_index >= len(recommendations):
    st.session_state.song_index = 0

if len(recommendations) > 0:

    song = recommendations[
        st.session_state.song_index
    ]

    iframe = f"""
    <iframe
        src="{song['link']}"
        width="100%"
        height="352"
        frameborder="0"
        allowfullscreen
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
    </iframe>
    """

    st.components.v1.html(
        iframe,
        height=400
    )

    if st.button("Next Song"):

        st.session_state.song_index += 1

        if (
            st.session_state.song_index
            >= len(recommendations)
        ):
            st.session_state.song_index = 0

        st.rerun()