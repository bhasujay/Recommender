import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


client_credentials_manager = SpotifyClientCredentials(client_id='a17d85fd78dc4e4f92217de5b3dfed2c',
                                                      client_secret='1616da6c8bb44ed98e89e7327b22d9a8')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


df = pd.read_csv('data/data.csv')
song_uris = df['spotify_track_uri'].tolist()
del df

non_dup_uris = []
for i in range(len(song_uris)):
    if song_uris[i] not in non_dup_uris:       
        non_dup_uris.append(song_uris[i])

non_dup_uris = non_dup_uris[1800:1806]
print(f"Number of songs {len(non_dup_uris)}\n\n\n\n")    
    
for i in range(len(non_dup_uris)):
    track_info = sp.track(non_dup_uris[i])
    song_name = track_info['name']
    
    print(f"index {i} - {non_dup_uris[i]} - {song_name}")