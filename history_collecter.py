import requests
from datetime import datetime, timedelta
from API_handler import get_access_token


access_token = get_access_token()
# Replace 'YOUR_ACCESS_TOKEN' with an actual OAuth token
headers = {
    'Authorization': f'Bearer {access_token}',
}

# Calculate the start date (30 days ago from today)
start_date = datetime.now() - timedelta(days=1)
start_timestamp = int(start_date.timestamp()) * 1000  # Convert to milliseconds

# Initialize an empty list to store tracks
listening_history = []

# Make requests until we have data from the past 30 days
while True:
    # Make a request to the recently played endpoint
    response = requests.get('https://api.spotify.com/v1/me/player/recently-played',
                            headers=headers,
                            params={'after': start_timestamp})
    
    if response.status_code != 200:
        print("Error:", response.status_code)
        break
    
    data = response.json()
    
    if not data['items']:
        # No more data available
        break
    
    # Filter tracks based on timestamp
    for item in data['items']:
        played_at = datetime.strptime(item['played_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if played_at > start_date:
            listening_history.append(item)
        else:
            # We have reached data older than 30 days
            break
    print(item)
    # Update start_timestamp for the next request
    start_timestamp = int(datetime.timestamp(played_at)) * 1000

# Process the listening history as needed
print(listening_history)
