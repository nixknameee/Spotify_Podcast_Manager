## The code imports necessary modules such as os, spotipy, dotenv, and tweepy. It loads environmental variables from the .env file, reads the Spotify client ID and client secret, creates an authentication instance with the SpotifyOAuth, and creates a list of podcasts to follow. It also creates a list of playlist IDs to search for matching names.

## After Twitter API authentication, the code loads the IDs of all tracks that have already been added to the playlists. It searches for the latest episodes of each podcast in the list and adds them to the "My Podcasts" playlist. If the track has already been added, it prints a message indicating that it was not added. If it has not been added, it tries to add it to any of the matching playlist IDs. If successful, it prints a message indicating that the track was added. If it fails, it prints a message indicating that it could not be added.

## Finally, the code tweets the name of the new episode and prints a message indicating whether the podcast was not found.

## Overall, the code seems to be a script for automatically adding the latest podcast episodes to a Spotify playlist and tweeting about them.



import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import tweepy

load_dotenv() # Laden Sie die .env-Datei in den Betriebssystemumgebungsvariablen

# Lese die Spotify-Client-ID und das Client-Geheimnis aus der Umgebungsvariable
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')


# Erstelle eine Spotify-Authentifizierungsinstanz mit der Umgebungsvariablen-Authentifizierung
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read playlist-read-private playlist-modify-public playlist-modify-private", client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8000/callback"))

# Erstelle eine Liste mit den Namen der Podcasts, die Sie verfolgen möchten
podcasts = ["Startup Insider", "Unicorn bakery - Der Starup Podcast für Gründer", "Handelsblatt Morning Briefing - News aus Wirtschaft, Politik und Finanzen"]

# Erstelle eine Liste von Wiedergabelisten-IDs, um später nach übereinstimmenden Namen zu suchen
playlist_ids = ['4xz5mhUSGWcERVXI7N0g9Z']
for item in sp.current_user_playlists()['items']:
    if item['name'] == 'DachPodcast':
        playlist_ids.append(item['id'])


# Twitter-API-Authentifizierung
auth = tweepy.OAuth1UserHandler(
    os.environ.get('TWITTER_API_KEY'),
    os.environ.get('TWITTER_API_SECRET_KEY'),
    os.environ.get('TWITTER_ACCESS_TOKEN'),
    os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    )

# Erstelle eine API-Instanz für Twitter
api = tweepy.API(auth)

# Laden die IDs aller bereits hinzugefügten Tracks
added_tracks = []
for pid in playlist_ids:
    playlist = sp.playlist_items(pid, fields="items(track(id))")
    for item in playlist['items']:
        added_tracks.append(item['track']['id'])

# Durchsuche jeden Podcast nach seinen neuesten Folgen und fügen Sie zur "Meine Podcasts"-Wiedergabeliste hinzu
for podcast in podcasts:
    results = sp.search(q=podcast, type='show')
    if results['shows']['total'] > 0:
        show_id = results['shows']['items'][0]['id']
        episodes = sp.show_episodes(show_id, limit=2)
        for episode in episodes['items']:
            track = episode['uri']
            track_name = episode['name']
            if track.split(':')[2] in added_tracks:
                print(f'{track_name} bereits hinzugefügt.')
            else:
                added = False
                for pid in playlist_ids:
                    if not added and sp.playlist_add_items(playlist_id=pid, items=[track]):
                        print(f'{track_name} erfolgreich hinzugefügt!')
                        added = True
                if not added:
                    print(f'Konnte {track_name} nicht hinzufügen.')

        print(f'Podcast {podcast} wurde nicht gefunden.')

            
        tweet = f"Neue Folge von {podcast} - {track_name} #podcast"
        api.update_status(status=tweet) 
else:
    print(f'Podcast {podcast} wurde nicht gefunden.')
