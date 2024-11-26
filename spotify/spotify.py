from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv,load_dotenv
import os

#inputing varaibles
dot_env = find_dotenv()
load_dotenv(dot_env)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_KEY = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")
billboard_link = "https://www.billboard.com/charts/hot-100/"
test_link = "https://www.billboard.com/charts/hot-100/2000-08-13/"
date = str(input("What time do you want to go back to? enter year in format YYYY-MM-DD  >>"))
year = date.split("-")[0]
billboard =requests.get(f"{billboard_link}/{date}/")
body = {
    "name": f"{date} Billboard 100",
    "description": f"Billboard 100 songs for the day {date}",
    "public": False
}
#webscraping the Billboard-100 website to get top-100 songs for a date
billboard_webpage = billboard.text
soup = BeautifulSoup(billboard_webpage,"html.parser")
soup_song = [i  for i in soup.select("div.o-chart-results-list-row-container ul.o-chart-results-list-row li.lrv-u-width-100p ul li.o-chart-results-list__item ") if i.select_one('h3.c-title')]
top100 = [{ i.select_one("h3#title-of-a-story").getText().strip(): i.select_one("span.c-label").getText().strip() } for i in soup_song] # type: ignore
top100_artist = [i.select_one("span.c-label").getText().strip() for i in soup_song]
top100_songs = [i.select_one("h3#title-of-a-story").getText().strip() for i in soup_song]
#Creating Spotify client
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, 
                                 client_secret=SPOTIFY_CLIENT_KEY, 
                                 redirect_uri=SPOTIPY_REDIRECT_URI,
                                 scope="playlist-modify-private", 
                                 show_dialog=True,
                                 cache_path="token.txt"))

user_id = sp.current_user()["id"]
playlist_uri = []

#creating playlist
for song in top100_songs:
    results = sp.search(q=f"track:{song} year:{year}",type="track")
    try:
        uri = results["tracks"]["items"][0]["uri"]
        playlist_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

PLAYLIST_ID = sp.user_playlist_create(user=user_id,public=False,name=f"{date} BillBoard-100")['id']

sp.user_playlist_add_tracks(playlist_id=PLAYLIST_ID,tracks=playlist_uri,user=user_id)

print(PLAYLIST_ID)


playlist_uri.clear()