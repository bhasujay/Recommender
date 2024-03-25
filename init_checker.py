import os
import requests

# this will check the initial state to start the program

def check(cwd,type):
    path = os.path.join(cwd,'data')
    data_list = os.listdir(path)
    
    if type == 'csv' and 'data.csv' in data_list:
        return True
    elif type == 'joblib' and 'model.joblib' in data_list:
        return True
    elif type == 'token' and 'tokens.txt' in data_list:
        return True
    else:
        return False
    
    
def api_access_avail(access_token):
    pass