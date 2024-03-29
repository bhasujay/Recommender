import requests
from API_handler import get_access_token

def get_song_info(song_uri, access_token):
    # Extract the song ID from the URI
    song_id = song_uri.split(':')[-1]

    # Make a request to the Spotify API
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(f'https://api.spotify.com/v1/tracks/{song_id}', headers=headers)
    song_info = response.json()

    # Extract and return relevant information about the song
    return {
        'name': song_info.get('name'),
        'artists': [artist['name'] for artist in song_info.get('artists')],
        'album': song_info.get('album', {}).get('name'),
        'release_date': song_info.get('album', {}).get('release_date'),
        'duration_ms': song_info.get('duration_ms'),
        'preview_url': song_info.get('preview_url')
    }

# Example usage:
access_token = get_access_token()
song_uri = 'spotify:track:7ucAyhKPjKsLrP14q4mcyo'  # Example song URI
song_info = get_song_info(song_uri, access_token)
print(song_info)
