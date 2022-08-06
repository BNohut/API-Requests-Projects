from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.client import Spotify

MY_USER_ID = "ur_spotify_user_id"
MY_CLIENT_ID = "ur_spotify_client_id"
MY_CLIENT_SECRET = "ur_spotify_client_secret_key"
redirected_url = "http://example.com/callback/"

# ------------------MAKING SOUP---------------------#
""" Takes the date of user select, finds the top 100 songs in that date"""

user_date = input("Which year do you want to travel to? Type the date in YYYY-MM-DD format:\n")

end_code = "https://www.billboard.com/charts/hot-100/"

response = requests.get(url=f"{end_code}{user_date}")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
class_of_songs_name = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet " \
                      "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis " \
                      "u-max-width-330 u-max-width-230@tablet-only"
all_h = soup.find_all(name="h3", class_=class_of_songs_name)
songs_list = [item.getText() for item in all_h]
song_names = []
replaced_song_names = [songs.replace("\n\n\t\n\t\n\t\t\n\t\t\t\t\t", "").replace("\t\t\n\t\n", "")
                       for songs in songs_list]

# --------------- AUTHORIZATION SPOTIFY ----------------#

sp = spotipy.oauth2.SpotifyOAuth(client_id=MY_CLIENT_ID, client_secret=MY_CLIENT_SECRET,
                                 redirect_uri=redirected_url, username=MY_USER_ID, scope="playlist-modify-private"
                                 )
auth_token = sp.get_cached_token()["access_token"]
# print(auth_token)
# --------------- ACCESS CURRENT USER INFO -------------#
"""Takes authorized 'sp' object and finds current user's 'User ID' on Spotify"""
sf = Spotify(auth_manager=sp)
user_id = sf.current_user()["id"]

# --------------- CREATE A PLAYLIST ON SPOTIFY --------#

header = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}

data = {
    "name": "Your_playlist_name",
    "public": False,
    "description": "My First Playlist that I have created it by Python Codes"
}

response = requests.post(url=f"https://api.spotify.com/v1/users/{user_id}/playlists", headers=header, json=data)
playlist_id = response.json()["id"]

# -------------- SEARCH IN SPOTIFY FOR SONGS ON BILLBOARD  --------------#
song_uris = []
for song in replaced_song_names:
    song_detail = {
        "q": song,
        "type": "track",
        "include_external": "audio",
        "limit": 1
    }
    response = requests.get(url="https://api.spotify.com/v1/search", params=song_detail, headers=header)
    contents = response.json()["tracks"]["items"]
    if len(contents) == 0:
        contents2 = f"There is not any track that named {song}"
    else:
        contents = contents[0]["uri"]
        song_uris.append(contents)
#
# -------------- ADD ALL SONGS TO CREATED PLAYLIST -------------------#
add_endcode = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
add_json = {
    "uris": song_uris
}
response = requests.post(url=add_endcode, json=add_json, headers=header)

