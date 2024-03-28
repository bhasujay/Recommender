from flask import Flask, redirect, request
import requests
import json
import time

app = Flask(__name__)

# Global variables 
user_info = {}
CLIENT_ID = 'a17d85fd78dc4e4f92217de5b3dfed2c'
CLIENT_SECRET = '1616da6c8bb44ed98e89e7327b22d9a8'

@app.route("/")
def index():
    return redirect("https://accounts.spotify.com/authorize?client_id=a17d85fd78dc4e4f92217de5b3dfed2c&response_type=code&redirect_uri=http://localhost:6767/callback&scope=user-read-private%20user-read-email%20user-read-currently-playing&state=123")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    access_token, refresh_token = get_access_token(code)
    user_info.update(get_user_info(access_token))
    save_tokens_to_file(access_token, refresh_token)
    return "<center><br><br><br><br><br><h1>Authorization is successful!<br>You can close this tab now</h1></center>"

def get_access_token(code):
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:6767/callback",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "show_dialog" : True
    }
    response = requests.post("https://accounts.spotify.com/api/token", data=payload)
    response_data = response.json()
    return response_data.get("access_token"), response_data.get("refresh_token")

def get_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user_data = response.json()
    user_info = {
        "username": user_data["display_name"],
        "email": user_data["email"],
        "profile_picture": user_data["images"][0]["url"]
    }

    with open("data/user_info.json", "w") as f:
        json.dump(user_info,f)
    
    return user_info

def save_tokens_to_file(access_token, refresh_token):
    with open("data/tokens.json", "w") as f:
        json.dump({"access_token": access_token, "refresh_token": refresh_token,"timestamp":(time.time()+3300)}, f)

# if __name__ == "__main__":
#     app.run(port=6767,debug=True)
