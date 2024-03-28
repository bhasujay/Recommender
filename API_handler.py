import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_access_token():
    
    if os.path.exists('data/tokens.json'):
        with open('data/tokens.json', 'r') as file:
            data = json.load(file)

        access_token = data['access_token']

        if time.time() < data['timestamp']:
            refresh_token = data['refresh_token']        
            token_refresh_url = "https://accounts.spotify.com/api/token"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
            access_token = requests.post(token_refresh_url, data=payload).json()["access_token"]
            with open("data/tokens.json", "w") as f:
                json.dump({"access_token": access_token, "refresh_token": refresh_token,"timestamp":(time.time()+3300)}, f)
        return access_token       
    else:
        return None
        

def get_current_track_info():
    
    access_token = get_access_token()
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    
    curr_track_data = {
        'track_name' : None,
        'album_name' : None,
        'artist_name' : None,
        'album_art_url' : None
        }
    
    if response.status_code == 200:
        data = response.json()
        curr_track_data = {
        'track_name' : data['item']['name'],
        'album_name' : data['item']['album']['name'],
        'artist_name' : ', '.join([artist['name'] for artist in data['item']['artists']]),
        'album_art_url' : data['item']['album']['images'][0]['url']
        }
        return curr_track_data
    else:
        return curr_track_data