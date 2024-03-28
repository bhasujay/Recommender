import os
import requests
import json
import time

from image_handler import remote_image

CLIENT_ID = 'a17d85fd78dc4e4f92217de5b3dfed2c'
CLIENT_SECRET = '1616da6c8bb44ed98e89e7327b22d9a8'

def download_profile_picture():
    with open('data/user_info.json','r') as file:
        data = json.load(file)
    print(f"downloaded profile picture = {remote_image(data['profile_picture']).download_image(filename='profile.png')}")


# the check_login fuction - this will check the access token state of the API
def check_login():
    if os.path.exists('data/tokens.json'):
        if not(os.path.exists('img/profile.png')):
            download_profile_picture()
        
        with open('data/tokens.json', 'r') as file:
            data = json.load(file)

        if time.time() < data['timestamp']:
            print("not expired")
            return True
        
        try:
            access_token = data['access_token']
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
            print("expired, refreshed into a new one")
            return True
        except:
            return False
    else:
        return False



# the check fuction - this will check the initial state to start the program
def check(cwd,type):
    path = os.path.join(cwd,'data')
    data_list = os.listdir(path)
    
    if type == 'csv' and 'data.csv' in data_list:
        return True
    elif type == 'joblib' and 'model.joblib' in data_list:
        return True
    else:
        return False