import tkinter.messagebox
import os
import time

from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import filedialog

from init_checker import check

# to check the initial state
cwd = os.getcwd()
checker = check(cwd)

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
            folder_btn.config(text='Import data',command=import_data,bg='#44FF88')
            path_label.config(fg='#000000')
        else:
            path_label.config(fg='#FF0000')
            
            
def import_data():
    
    ###############################################
    
    if bar['value'] > 0:
        bar['value'] -= bar['value']
    with open(os.path.join(cwd,'data','data.csv'), 'w') as f:
        pass
    for i in range(10000):
        time.sleep(0.0001)
        bar['value'] += 1/100
        win.update_idletasks()
    
    ###############################################
    
    folder_btn.config(text='Imported',command=showinfo,fg='#666666',bg='#F0F0F0')
    train_btn.config(text='Train',command=train_execute,bg='#44FF88',fg='#000000')
    
    
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

if checker.check_data('data'):
    folder_btn = Button(frame_btns,text='Imported',command=showinfo,fg='#666666')
    folder_btn.place(relheight=0.5,relwidth=0.2,relx=0.1,rely=0.25)
else:
    folder_btn = Button(frame_btns,text='Select folder',command=select_folder)
    folder_btn.place(relheight=0.5,relwidth=0.2,relx=0.1,rely=0.25)

if checker.check_model('data'):
    train_btn = Button(frame_btns,text='Trained',fg='#666666',command=showinfo)
    train_btn.place(relheight=0.5,relwidth=0.2,relx=0.35,rely=0.25)
elif checker.check_data('data'):
    train_btn = Button(frame_btns,text='Train',command=train_execute)
    train_btn.place(relheight=0.5,relwidth=0.2,relx=0.35,rely=0.25)
else:
    train_btn = Button(frame_btns,text='Train',fg='#999999')
    train_btn.place(relheight=0.5,relwidth=0.2,relx=0.35,rely=0.25)

if checker.check_model('data'):
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

if checker.check_model('data') or checker.check_data('data'):
    bar['value'] = 100


win.mainloop()