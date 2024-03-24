import os

# this will check the initial state to start the program

class check:
    
    def __init__(self,path):
        self.path = path
        
    def check_data(self,folder):
        self.dir = os.path.join(self.path,folder)
        self.data_list = os.listdir(self.dir)
        
        if 'data.csv' in self.data_list:
            return True
        else:
            return False
        
    def check_model(self,folder):
        self.dir = os.path.join(self.path,folder)
        self.data_list = os.listdir(self.dir)
        
        if 'model.joblib' in self.data_list:
            return True
        else:
            return False
        
    def check_spotifyAPI_availability(self,folder):
        pass