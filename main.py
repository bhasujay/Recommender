import os
import sys
import time
import pandas as pd
import glob
import threading
import json
import webbrowser

# from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime 
from PIL import ImageTk

from start_handler import *
from login import *
from image_handler import remote_image,local_image
from API_handler import *

# to check the initial state
cwd = os.getcwd()
csv = check(cwd,'csv')
model = check(cwd,'joblib')
logged = check_login()


def start_server():
    app.run(port=6767)
    
def login():
    webbrowser.open_new("http://127.0.0.1:6767")  
    messagebox.showinfo("Reload","The program needs to be reloaded.\nPress the reload button")
    login_btn.config(text="Reload",command=reload,fg='#FFFFFF',bg='#DE4242')
    
def reload():
    win.destroy()
    python = sys.executable
    os.execl(python, python, *sys.argv)  

################################################################################################################################################
    
def select_folder():
    global path
    
    path = filedialog.askdirectory() 
    path_label.config(text=path)
    
    if path:
        files = os.listdir(path)
        if files[0].split('.')[-1].lower() == 'json':
            folder_btn.config(text='Import data',command=thread_import_data,bg='#44FF88')
            path_label.config(fg='#000000')
        else:
            path_label.config(fg='#FF0000')
         
def thread_import_data():
    threading.Thread(target=import_data).start()         
def import_data():
    global path
    
    folder_btn.config(text='Importing',command=showwarning,bg='#FF2222')
    if bar['value'] > 0:
        bar['value'] -= bar['value']
    
    file_paths = glob.glob(os.path.join(path,'*.json'))
    dfs = []
    path_label.config(text="Collecting files")
    for i in range(len(file_paths)):
        df = pd.read_json(file_paths[i])
        dfs.append(df)
        
        bar['value'] += 1/len(file_paths)*100
        win.update_idletasks()
        
    df = pd.concat(dfs, ignore_index=True)
    path_label.config(text="Removing duplicates")
    df = df.drop_duplicates()
    length = len(df)
    
    artist_list = []
    uri_list = []
    album_list = []
    artists = 0
    albums = 0
    songs = 0
    ms_played = 0
    
    if bar['value'] > 0:
        bar['value'] -= bar['value']
    path_label.config(text="Deleting unnecessary data fields")
    
    rem_list = ['username','platform','conn_country','ip_addr_decrypted','user_agent_decrypted','master_metadata_track_name','episode_name','episode_show_name','spotify_episode_uri','reason_start','reason_end','shuffle','skipped','offline','offline_timestamp','incognito_mode']
    for i in range(len(rem_list)):
        del df[rem_list[i]]
        
        bar['value'] += 1/len(rem_list)*100
        win.update_idletasks()
        
    df['month'] = ''
    df['day'] = ''
    df['hour'] = ''
    df['min'] = ''

    if bar['value'] > 0:
        bar['value'] -= bar['value']
    path_label.config(text=f"importing {length} data")
    count = 1

    for index in df.index:

        timestamp = datetime.strptime(str(df.loc[index, 'ts']), '%Y-%m-%dT%H:%M:%SZ')
        artist = df.loc[index, 'master_metadata_album_artist_name']
        album = df.loc[index, 'master_metadata_album_album_name']
        uri = str(df.loc[index, 'spotify_track_uri']).split(':')[-1]
        
        ms_played += int(df.loc[index, 'ms_played'])
        if artist not in artist_list:
            artist_list.append(artist)
            artists += 1
        if album not in album_list:
            album_list.append(album)
            albums += 1
        if uri not in uri_list:
            songs += 1
            uri_list.append(uri)
        
        if uri == 'None':
            df = df.drop(index)
            continue
            
        df.loc[index, 'spotify_track_uri'] = uri
        df.loc[index, 'month'] = timestamp.month
        df.loc[index, 'day'] = timestamp.weekday()
        df.loc[index, 'hour'] = timestamp.hour
        df.loc[index, 'min'] = timestamp.minute
            
        path_label.config(text=f"{count} out of {length} data have been imported")
        bar['value'] += 1/length*100
        count += 1
        win.update_idletasks()
        
    del df['master_metadata_album_artist_name']
    del df['master_metadata_album_album_name']
    del df['ts']
    del artist_list
    del uri_list
    del album_list

    order = ['month','day','hour','min','spotify_track_uri']
    df = df[order]
    
    path_label.config(text=f"Saving Data...........")
    bar['value'] = 100
    win.update_idletasks()

    csv_path = os.path.join(cwd,'data/data.csv')
    df.to_csv(csv_path, index=False)
    del df

    with open(os.path.join(cwd,'data/report.txt'), 'w') as f:
        f.write(f"Listened for {ms_played / (1000 * 60)} minutes.\n{artists} Artists.\n{songs} Songs.\n{albums} Albums.\n{length} of streams")
    
    
    folder_btn.config(text='Imported',command=showinfo,fg='#666666',bg='#F0F0F0')
    train_btn.config(text='Train',command=train_execute,bg='#44FF88',fg='#000000')
    time.sleep(1.5)
    path_label.config(text=f"Your data is saved!")
    
def train_execute():
    
    ###############################################
    
    if bar['value'] > 0:
        bar['value'] -= bar['value']
    with open(os.path.join(cwd,'data','model.joblib'), 'w') as f:
        pass
    for i in range(100):
        time.sleep(0.0001)
        bar['value'] += 1
        win.update_idletasks()

    ###############################################
    path_label.config(text="The Model is now trained!")
    train_btn.config(text='Trained',command=showinfo,fg='#666666',bg='#F0F0F0')
    rec_btn.config(fg='#000000',bg='#1ED760',command=recommend_execute)
     
def recommend_execute():
    
    ###############################################
    
    print("Song name")
    
    ###############################################
    
################################################################################################################################################
    
def showinfo():
    messagebox.showinfo(title=None,message="you completed that task!")

def showwarning():
    messagebox.showwarning(title='Warning',message="This task is still running!")

def logout():
    result = messagebox.askquestion("Confirmation", "Do you want to Log out?")
    if result == 'yes':
        os.remove('img/profile.png')
        os.remove('data/tokens.json')
        os.remove('data/user_info.json')
        reload()

def get_current():
    if logged:
        threading.Thread(target=update_curr_track_details).start()
def update_curr_track_details():
    data = get_current_track_info()
    if data['track_name'] is not None:
        album_photo = remote_image(data['album_art_url']).get_image(120,120,'album_art')
        tk_album_photo = ImageTk.PhotoImage(album_photo)
        al_photo.config(image=tk_album_photo)
        al_photo.image = tk_album_photo
            
        if len(data['track_name']) > 30:
            song = f"{data['track_name'][0:30]}\n        {data['track_name'][30:-1]}"
        else:
            song = data['track_name']
            
        if ',' in data['artist_name']:
            artists = data['artist_name'].split(',')
            artists = [value.strip() for value in artists]
            if len(artists) > 3:
                artist = f"{artists[0]}, {artists[1]}, {artists[2]},\n        {', '.join(artists[3:])}"
            else:
                artist = ', '.join(artists)
        else:
            artist = data['artist_name']
            
        text = f"Song : {song}\nArtist : {artist}\nAlbum : {data['album_name']}"
        curr_info.config(text=text,justify='left')        
    

################################################################################################################################################


if logged:
    with open('data/user_info.json', "r") as json_file:
        user_info = json.load(json_file)    
    
    if os.path.exists('img/profile.png'):
        profile_photo = local_image('img/profile.png').get_pro_image()
    else:
        profile_photo = local_image('img/default_profile.png').get_pro_image()
    
else:
    
    profile_photo = local_image('img/default_profile.png').get_pro_image()
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    


################################################################################################################################################

win = Tk()
win.title('Recommender')
win.geometry('700x550')
win.resizable(False , False)

tk_profile_photo = ImageTk.PhotoImage(profile_photo)
tk_album_photo = ImageTk.PhotoImage(local_image('img/default_album_art.png').get_album_art())
tk_refresh_img = ImageTk.PhotoImage(local_image('img/refresh.png').get_image(30,30))


if logged:
    pro_photo = Label(win,image=tk_profile_photo)
    pro_photo.place(relx=0.1,rely=0.04)
    
    name = Label(win,text=f"{user_info["username"]} | {user_info["email"]}", font=('Kristen ITC', '11'))
    name.place(relx=0.18,rely=0.06)
    
    login_btn = Button(win,text="Log out",font=('arial','13'),command=logout,bg='#1DB954')
    login_btn.place(relx=0.75,rely=0.06,relheight=0.05,relwidth=0.15)
    
else:
    pro_photo = Label(win, image=tk_profile_photo)
    pro_photo.place(relx=0.1,rely=0.04)
    
    name = Label(win,text="User | Email", font=('Kristen ITC', '11'))
    name.place(relx=0.18,rely=0.06)
    
    login_btn = Button(win,text="Login",font=('arial','13'),command=login)
    login_btn.place(relx=0.75,rely=0.06,relheight=0.05,relwidth=0.15)


al_photo = Label(win,image=tk_album_photo)
al_photo.place(relx=0.15,rely=0.15)

get_current()
    
ref_button = Button(image=tk_refresh_img,command=get_current,borderwidth=0)
ref_button.place(relx=0.8,rely=0.135)

curr_info = Label(text='Song :\nArtist :\nAlbum :',font=('Kristen ITC', '11'),justify='left')
curr_info.place(relx=0.35,rely=0.19)



frame_btns = Frame(win,background='#FFFFFF')

if csv:
    folder_btn = Button(frame_btns,text='Imported',command=showinfo,fg='#666666')
    folder_btn.place(relheight=0.5,relwidth=0.2,relx=0.1,rely=0.25)
else:
    folder_btn = Button(frame_btns,text='Select folder',command=select_folder)
    folder_btn.place(relheight=0.5,relwidth=0.2,relx=0.1,rely=0.25)

if model:
    train_btn = Button(frame_btns,text='Trained',fg='#666666',command=showinfo)
    train_btn.place(relheight=0.5,relwidth=0.2,relx=0.35,rely=0.25)
elif csv:
    train_btn = Button(frame_btns,text='Train',command=train_execute)
    train_btn.place(relheight=0.5,relwidth=0.2,relx=0.35,rely=0.25)
else:
    train_btn = Button(frame_btns,text='Train',fg='#999999')
    train_btn.place(relheight=0.5,relwidth=0.2,relx=0.35,rely=0.25)

if logged and model:
    rec_btn = Button(frame_btns,text='Recommend',command=recommend_execute, font=('arial','13'),fg='#000000',bg='#1DB954')
    rec_btn.place(relheight=0.5,relwidth=0.2,relx=0.75,rely=0.25)
else: 
    rec_btn = Button(frame_btns,text='Recommend', font=('arial','13'),fg='#999999')
    rec_btn.place(relheight=0.5,relwidth=0.2,relx=0.75,rely=0.25)

frame_btns.place(relx=0.1,rely=0.4,relheight=0.1,relwidth=0.8)


path_label = Label(win,text='',font=('Calibri Light (Headings)','8'))
path_label.place(relx=0.11,rely=0.5)
if model:
    path_label.config(text="The Model is now trained!")

bar = Progressbar(win, orient=HORIZONTAL , length=562)
bar.place(relx=0.1,rely=0.53)

if csv or model:
    bar['value'] = 100

win.mainloop()