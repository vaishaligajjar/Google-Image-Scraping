
from flask import Flask , render_template,request, jsonify
from flask_cors import CORS , cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as ureq
import logging
logging.basicConfig(filename="scapper.log", level = logging.INFO)
import os

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review", methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        try:

            query = request.form['content'].replace(" ", "")

            make_directory = "Images/"
            if not os.path.exists(make_directory):
                os.makedirs(make_directory)

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

            response = requests.get(f"https://www.google.com/search?sca_esv=2fcb7b144273d9a6&sca_upv=1&rlz=1C1ONGR_enIN1067IN1067&sxsrf=ADLYWILiM8yQhwPfsgLl3NyGPTULjGqMMA:1725640619589&q={query}&udm=2&fbs=AEQNm0DSjjYWCybNh4Y2in02N243-OHmPxREG1BKYr-Kgpdbh-COBiIiY8Fo3IG2RaEyCjej1JUx8BX1u76p09NZAhv-YNiGIgZaBVjE1yk17r1Pes7N9RcUvgmVqNTHO5N_g-kDyYgYdm4Op_EcGu7hted7E2mWk79xdPeBeYAs19hMVEDpflJ2rmVJ8xnZa2uRFEpNko7gAJheNEfaMN8eCXu7CiQQ6A&sa=X&ved=2ahUKEwj9y4-h4K6IAxXERWwGHaIPIA4QtKgLegQIBxAB&biw=1366&bih=607&dpr=1")

            Soup = BeautifulSoup(response.content, "html.parser")
            search_image = Soup.find_all("img")
            del search_image[0]
            image_list = []
            for index, image_tags in enumerate(search_image):
                url_link = image_tags['src']
                url_data = requests.get(url_link).content
                my_dict = {"index": index, "image": url_data}
                image_list.append(my_dict)

                with open(os.path.join(make_directory, f"{query}_{search_image.index(image_tags)}.jpg"),'wb') as f:
                    f.write(url_data)

            return "image loaded"
        except Exception as e:
            logging.info(e)
            return "something is wrong"
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)

