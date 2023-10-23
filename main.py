from bs4 import BeautifulSoup
import requests
from keys import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# ------Take user input for date----------
user_date = input("Enter the date you want the songs from (format YY-MM-DD): ")
# print(user_date)
#
# -------------use request to get data from billboard-----------------
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}/")
data = response.text
#
# ------------Using BeautifulSoup to get data-------------------
soup = BeautifulSoup(data, "html.parser")

# -----------getting all the music titles---------------
all_title = soup.select(selector="li ul li h3")
title = [title.string.strip() for title in all_title]
music_title = []
for x in title:
    if "(From " in x:
        music_title.append(x.split("(")[0])
    else:
        music_title.append(x)


# --------------Spotipy-----------------------

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri="http://localhost:3000",
                                               scope=scope))

sp2 = spotipy.oauth2.SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)

user_id = spotipy_user_id
playlist_name = f"{user_date} - Billboard 100"
sp_user_playlists = sp.current_user_playlists()["items"]
user_playlists = [sp_user_playlists[x]["name"] for x in range(len(sp_user_playlists))]
user_playlist_id = [sp_user_playlists[x]["id"] for x in range(len(sp_user_playlists))]
# print(user_playlists)

if playlist_name not in user_playlists:
    sp.user_playlist_create(user=user_id, name=playlist_name)
    for x in range(len(sp.current_user_playlists()["items"])):
        if sp.current_user_playlists()["items"][x]["name"] == playlist_name:
            playlist_id = sp.current_user_playlists()["items"][x]["id"]
    print("playlist made")
else:
    print("playlist already present")
    playlist_id = user_playlist_id[user_playlists.index(playlist_name)]

# print(playlist_id)

song_uri = []
for name in music_title:
    print(name)
    results = sp.search(q='track:' + name, type='track')
    try:
        items = results['tracks']['items'][0]
        track_uri = items["uri"]
        song_uri.append(track_uri)
    except IndexError:
        print("NO such record")
# print(song_uri)
sp.playlist_add_items(playlist_id=playlist_id, items=song_uri)
