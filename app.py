import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as ureq
import logging 
import pymongo
import os 
from flask import Flask,jsonify,render_template,request
from flask_cors import CORS,cross_origin
import logging 

logging.basicConfig(filename="img_scrapper.log", level=logging.INFO)

app = Flask(__name__)
@app.route("/",methods = ['GET'])
def homepage():
    return render_template("index.html")
# directory for images 
images = "images/"
if not os.path.exists(images):
    os.makedirs(images)
@app.route("/review", methods= ['POST','GET'])
def index():
    if request.method =='POST':
        try:
            query = request.form['content'].replace(" ","") # search query for images 
            
            save_directory = "images/" # crating a directory in which images stored 
        
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
                
            header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"} # fake user agent to avoid getting blocked by the google 
            
            response = requests.get(f"https://www.google.com/search?q={query}&sca_esv=9c09e8356b840daa&rlz=1C1CHBF_enIN1073IN1073&udm=2&biw=1440&bih=739&sxsrf=ACQVn0_nxu4z8nMGBEROKwYUwSfa56sNWg%3A1708782382716&ei=LvPZZaCmK6COseMPyOG3yAU&ved=0ahUKEwig9a23jsSEAxUgR2wGHcjwDVkQ4dUDCBA&uact=5&oq=kshitij&gs_lp=Egxnd3Mtd2l6LXNlcnAiB2tzaGl0aWoyCBAAGIAEGMcFMggQABiABBjHBTIIEAAYgAQYxwUyCBAAGIAEGMcFMggQABiABBjHBTIFEAAYgAQyCBAAGIAEGMcFMggQABiABBjHBTIIEAAYgAQYxwUyCBAAGIAEGMcFSMUiULEJWNYfcAJ4AJABBJgBqQKgAZsUqgEFMC40Lji4AQPIAQD4AQGYAgqgApYNqAIKwgIEEAAYA8ICBxAAGIAEGBjCAgQQIxgnwgIHEAAYAxjHBcICChAAGIAEGBgYxwXCAgcQIxjqAhgnwgIHEAAYgAQYAsICCxAAGIAEGMcFGLEDwgIKEAAYgAQYAhixA5gDBogGAZIHBTIuNC40&sclient=gws-wiz-serp")
            data = (BeautifulSoup(response.content,'html.parser')) #printing if we getting the response or not 

            images_tags = data.find_all("img")
            del images_tags[0] # deleting first element becz it is a header 
            img_Mongodb = []

            for i in images_tags:
                image_url = i['src']
                image_data = requests.get(image_url).content
                mydict = {"index":image_url,"image":image_data}
                img_Mongodb.append(dict)
                with open(os.path.join(images,f"{query}_{images_tags.index(i)}.jpg"),"wb") as f:
                    f.write(image_data)
                    
            client = pymongo.MongoClient("mongodb+srv://kshitijk146:kshitij@cluster0.uf1akim.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            db = client['image_scrap']
            collection = db["data"]
            collection.insert_many(image_data)
            
            return 'image loaded'
        except Exception as e:
            logging.info(e)
            return 'image loaded'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
