import requests
from io import BytesIO
from PIL import Image, ImageDraw

class remote_image:
    
    def __init__(self,url):
        self.url = url
    
    def get_image(self,width,height,type):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                image_bytes = BytesIO(response.content)
                self.image = Image.open(image_bytes)
            else:
                self.image = Image.open(f"img/default_{type}.png")
        except Exception as e:
            print(e)
            self.image = Image.open(f"img/default_{type}.png")
            return None
            
        self.image = self.image.resize((width,height))        
        return self.image
    
    def download_image(self,filename):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                with open(('img/'+filename), 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print("Failed to download the image. Status code:", response.status_code)
                return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False
        
class local_image:
    
    def __init__(self,path):
        self.path = path
        
    def get_pro_image(self):
        image = Image.open(self.path)
        image = image.resize((40,40),Image.Resampling.LANCZOS)
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + image.size, fill=255)
        image = Image.composite(image, Image.new('RGB', mask.size, '#F0F0F0'), mask)
        return image
    
    def get_album_art(self):
        image = Image.open(self.path)
        image = image.resize((120,120))
        return image
    
    def get_image(self,w,h):
        image = Image.open(self.path)
        image = image.resize((w,h))
        return image
