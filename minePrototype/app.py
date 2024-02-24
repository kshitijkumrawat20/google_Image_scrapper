import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as ureq
import logging 
import pymongo
import os 
from flask import Flask,jsonify,render_template,request
from flask_cors import CORS,cross_origin
import logging 

# logging.basicConfig(filename="img_scrapper.log", level=logging.INF

    
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

query = "kshitij"
response = requests.get(f"https://www.google.com/search?q={query}&sca_esv=9c09e8356b840daa&rlz=1C1CHBF_enIN1073IN1073&udm=2&biw=1440&bih=739&sxsrf=ACQVn0_nxu4z8nMGBEROKwYUwSfa56sNWg%3A1708782382716&ei=LvPZZaCmK6COseMPyOG3yAU&ved=0ahUKEwig9a23jsSEAxUgR2wGHcjwDVkQ4dUDCBA&uact=5&oq=kshitij&gs_lp=Egxnd3Mtd2l6LXNlcnAiB2tzaGl0aWoyCBAAGIAEGMcFMggQABiABBjHBTIIEAAYgAQYxwUyCBAAGIAEGMcFMggQABiABBjHBTIFEAAYgAQyCBAAGIAEGMcFMggQABiABBjHBTIIEAAYgAQYxwUyCBAAGIAEGMcFSMUiULEJWNYfcAJ4AJABBJgBqQKgAZsUqgEFMC40Lji4AQPIAQD4AQGYAgqgApYNqAIKwgIEEAAYA8ICBxAAGIAEGBjCAgQQIxgnwgIHEAAYAxjHBcICChAAGIAEGBgYxwXCAgcQIxjqAhgnwgIHEAAYgAQYAsICCxAAGIAEGMcFGLEDwgIKEAAYgAQYAhixA5gDBogGAZIHBTIuNC40&sclient=gws-wiz-serp")

data = (BeautifulSoup(response.content,'html.parser')) #printing if we getting the response or not 

images_tags = data.find_all("img")
# print(len(images_tags))
del images_tags[0] # deleting first element becz it is a header 
img_Mongodb = []

for i in images_tags:
    image_url = i['src']
    image_data = requests.get(image_url).content
    mydict = {"index":image_url,"image":image_data}
    img_Mongodb.append(dict)
    with open(os.path.join(images,f"{query}_{images_tags.index(i)}.jpg"),"wb") as f:
        f.write(image_data)

# client = pymongo.MongoClient("")
# db = client["image_scrap"]
# collection_image = db["image_scrap"]
# collection_image.insert_many(img_Mongodb ) 