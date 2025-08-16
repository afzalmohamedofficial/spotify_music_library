from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import streamlit as st

# Load enviorment variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
SP = spotipy.Spotify(auth_manager=auth_manager)

       
def get_artist_top_tracks(artist_id):
    try:
        results = SP.artist_top_tracks(artist_id, country ="IN")
        tracks = [{"song": track["name"], "link": track["external_urls"]["spotify"]} for track in results["tracks"]]
        return pd.DataFrame(tracks)
    except Exception as e:
        st.error(f"Error fetching top tracks: {e}")
        return pd.DataFrame()

def get_artist_albums(artist_id):
    
    albums = []
    results = SP.artist_albums(artist_id, album_type="album")
    albums.extend(results["items"])

    while results["next"]:
        results = SP.next(results)
        albums.extend(results["items"])

    all_albums= []
    
    for album in albums:
        all_albums.append({"id": album["id"], "Album_name": album["name"], "link": album["external_urls"]["spotify"]})

    return all_albums

def get_artist_albums_by_year(artist_id, target_year):
    str_target_year = str(target_year)
    albums = []
    results = SP.artist_albums(artist_id, album_type="album", country="IN")
    albums.extend(results["items"])

    while results["next"]:
        results = SP.next(results)
        albums.extend(results["items"])

    album_by_year = []

    for album in albums:
        release_year = album["release_date"][:4]
        if release_year == str_target_year:
            album_by_year.append({"id": album["id"], "Album_name": album["name"], "year": album["release_date"][:4], "link": album["external_urls"]["spotify"]})


        
    return  album_by_year

def get_album_tracks(album_id):
    tracks = []

    results = SP.album_tracks(album_id)
    tracks.extend(results["items"])
    
    while results["next"]:
        results = SP.next(results)
        tracks.extend(results["items"])
    
    

    return tracks

@st.cache_data
def get_all_artist_tracks(artist_id):
    all_tracks = []

    albums = get_artist_albums(artist_id)

    for album in albums:
        album_tracks = get_album_tracks(album["id"])
        for track in album_tracks:
            all_tracks.append({"track_name": track["name"], "Album_name": album["Album_name"], "link": track["external_urls"]["spotify"]})


    return all_tracks
    
@st.cache_data(show_spinner=False)
def get_all_artist_tracks_by_year(artist_id, target_year):
    all_tracks = []

    albums = get_artist_albums_by_year(artist_id, target_year)

    for album in albums:
        album_tracks = get_album_tracks(album["id"])
        for track in album_tracks:
            all_tracks.append({"track_name": track["name"], "Album_name": album["Album_name"], "Release_year": album["year"], "link": track["external_urls"]["spotify"]})


    return all_tracks

