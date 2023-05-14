# Podcast Playlist Manager
This script uses the Spotify API to automatically add new episodes of podcasts you follow to your Spotify playlist.

## Setup
Create a new Spotify app on the Spotify Developer Dashboard and note down the client ID and client secret.

Install the spotipy package by running pip install spotipy.

## Usage
1. Add the names of the podcasts you want to follow to the podcasts list.

2. Add the IDs of your Spotify playlists to the playlist_ids list to search for matching names and add new episodes.

3. Run the script: python main.py.

4. The script will automatically add new episodes of the podcasts you follow to your Spotify playl ist.

5. You can customize the scope of the authentication by modifying the SpotifyOAuth parameters in the sp instantiation.

6. The script also uses the dotenv package to load environment variables from a .env file. Create a .env file in the same directory as the main.py file and add the following variables:

> CLIENT_ID=<your_spotify_client_id>

> CLIENT_SECRET=<your_spotify_client_secret>

7. Optionally, you can also add your Twitter API credentials to tweet the name of the new episode. Install the tweepy package by running pip install tweepy.

8. Run the script and enjoy your customized podcast playlist!
