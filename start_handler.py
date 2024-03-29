import os
import requests
import json
import time

from image_handler import remote_image
from API_handler import get_access_token


def download_profile_picture():
    with open('data/user_info.json','r') as file:
        data = json.load(file)
    print(f"downloaded profile picture = {remote_image(data['profile_picture']).download_image(filename='profile.png')}")


# the check_login fuction - this will check the access token state of the API
def check_login():    
    if get_access_token() is None:
        return False
    else:
        if not(os.path.exists('img/profile.png')):
            download_profile_picture()
        return True



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