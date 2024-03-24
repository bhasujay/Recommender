import tkinter.messagebox
import os
import time
import pandas as pd
import glob
import threading

from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import filedialog
from datetime import datetime 

from init_checker import *

# to check the initial state
cwd = os.getcwd()
csv = check(cwd,'csv')
model = check(cwd,'joblib')

def login_execute():
    
    ##############################################
    
    print("Logged in")
    
    ##############################################
    
    name.config(text="User : Bhazu")
    email.config(text="Email : bhasumagic@gmail.com")
    login_btn.config(command=showinfo,fg='#888888',bg='#11EE55',text="Logged in")
    
    
def select_folder():
    global path
    
    path = filedialog.askdirectory() 
    path_label.config(text=path)
    
    if path:
        files = os.listdir(path)
        if files[0].split('.')[-1].lower() == 'json':
            folder_btn.config(text='Import data',command=start_import_data,bg='#44FF88')
            path_label.config(fg='#000000')
        else:
            path_label.config(fg='#FF0000')

           
def start_import_data():
    threading.Thread(target=import_data).start()         
def import_data():
    global path
    
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
    df['min_frame'] = ''

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

        if length < 5000:
            df.loc[index, 'min_frame'] = timestamp.minute // 30
        elif length < 10000:
            df.loc[index, 'min_frame'] = timestamp.minute // 20
        elif length < 50000:
            df.loc[index, 'min_frame'] = timestamp.minute // 10
        else:
            df.loc[index, 'min_frame'] = timestamp.minute // 5
            
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

    order = ['month','day','hour','min_frame','spotify_track_uri']
    df = df[order]
    
    path_label.config(text=f"Saving Data...........")
    bar['value'] = 100
    win.update_idletasks()

    csv_path = os.path.join(cwd,'data/data.csv')
    df.to_csv(csv_path, index=False)
    del df

    with open(os.path.join(cwd,'data/report.txt'), 'w') as f:
        f.write(f"Listened for {ms_played / (1000 * 60)} minutes.\n{artists} Artists.\n{songs} Songs.\n{albums} Albums.")
    

    ###############################################
    
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
    
    train_btn.config(text='Trained',command=showinfo,fg='#666666',bg='#F0F0F0')
    rec_btn.config(fg='#000000',bg='#1ED760',command=recommend_execute)
    
    
def recommend_execute():
    
    ###############################################
    
    print("Song name")
    
    ###############################################
    
    
def showinfo():
    tkinter.messagebox.showinfo(title=None,message="you completed that task!")
            

win = Tk()
win.title('Recommender')
win.geometry('700x500')
win.resizable(False , False)


name = Label(win,text="User : None", font=('Arial', '13'))
name.place(relx=0.1,rely=0.08)

email = Label(win,text="Email : None", font=('Arial', '13'))
email.place(relx=0.3,rely=0.08)

login_btn = Button(win,text="Log in",font=('arial','13'),command=login_execute)
login_btn.place(relx=0.75,rely=0.08,relheight=0.05,relwidth=0.15)


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

if model:
    rec_btn = Button(frame_btns,text='Recommend', font=('arial','13'),bg='#1ED760',command=recommend_execute)
    rec_btn.place(relheight=0.5,relwidth=0.2,relx=0.75,rely=0.25)
else:
    rec_btn = Button(frame_btns,text='Recommend', font=('arial','13'),fg='#999999')
    rec_btn.place(relheight=0.5,relwidth=0.2,relx=0.75,rely=0.25)

frame_btns.place(relx=0.1,rely=0.45,relheight=0.1,relwidth=0.8)


path_label = Label(win,text='')
path_label.place(relx=0.11,rely=0.56)

bar = Progressbar(win, orient=HORIZONTAL , length=562)
bar.place(relx=0.1,rely=0.6)

if csv or model:
    bar['value'] = 100


win.mainloop()