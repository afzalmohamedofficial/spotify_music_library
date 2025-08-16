import streamlit as st
import json
from spotify_music_api import get_artist_top_tracks, get_artist_albums , get_all_artist_tracks, get_all_artist_tracks_by_year
from datetime import datetime
import pandas as pd

# load css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply CSS
local_css("style.css")

with open("./assets/tamil_music_artist_id.json", "r") as file:
    artist_list = json.load(file)

artist_dict = {artist["artist_name"]:artist["artist_id"] for artist in artist_list}

# Set default session state
st.session_state.setdefault("page", "top_tracks")
st.session_state.setdefault("artist_id", list(artist_dict.values())[0])

st.title("Tamil Music Library")

option = st.selectbox("Select Artist", sorted(artist_dict.keys()))

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("assets/images/img_1.jpg", use_column_width=True)
    if st.button("Top 10 tracks", key="top_tracks"):
        st.session_state["page"] = "top_tracks"

with col2:
    st.image("assets/images/img_1.jpg", use_column_width=True)
    if st.button("All Album", key="all_album"):
        st.session_state["page"] = "all_album"

with col3:
    st.image("assets/images/img_1.jpg", use_column_width=True)
    if st.button("All songs", key="all_songs"):
        st.session_state["page"] = "all_songs"
      
with col4:
    st.image("assets/images/img_1.jpg", use_column_width=True)
    if st.button("Song By Year", key="song_year"):
        st.session_state["page"] = "song_year"


# Navigation
if "page" in st.session_state:

    if st.session_state["page"] == "top_tracks":
        artist_id = artist_dict[option]
        album_df = get_artist_top_tracks(artist_id)
        st.data_editor(album_df, column_config={"link": st.column_config.LinkColumn("spotify link")}, hide_index=True)
    
    elif st.session_state["page"] == "all_album":
        artist_id = artist_dict[option]
        all_album_list = get_artist_albums(artist_id)
        album_df = pd.DataFrame(all_album_list)[["Album_name", "link"]]
        st.data_editor(album_df, column_config={"link": st.column_config.LinkColumn("spotify link")}, hide_index=True)
    
    elif st.session_state["page"] == "all_songs":
            artist_id = artist_dict[option]
            track_df = get_all_artist_tracks(artist_id)
            st.data_editor(track_df, column_config={"link": st.column_config.LinkColumn("spotify link")}, hide_index=True)


    elif st.session_state["page"] == "song_year":
        artist_id = artist_dict[option]
        song_by_year = st.slider("Select Year", 1900, datetime.now().year, value=datetime.now().year)
        if st.button("Submit", key="year_search"):
            with st.spinner("Fetching Tracks"):
                track_list = get_all_artist_tracks_by_year(artist_id, song_by_year)
                track_df = pd.DataFrame(track_list)
            if not track_df.empty:
                st.data_editor(track_df, column_config={"link": st.column_config.LinkColumn("spotify link")}, hide_index=True)
            else:
                st.write(f"No songs found in {song_by_year}.")






    
    










