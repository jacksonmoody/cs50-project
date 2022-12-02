from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        response = requests.get("https://cs50-project-backend.herokuapp.com/")
        response = response.json()
        try:
            nyt_response = response["nyt_api"]
            wiki_response = response["wiki_api"]
            youtube_response = response["youtube_api"]

            num_nyt = random.randint(0, len(nyt_response) - 1)
            num_wiki = random.randint(0, len(wiki_response) - 1)
            num_yt = random.randint(0, len(youtube_response) - 1)

            return render_template("results.html", nyt_response=nyt_response[num_nyt], wiki_response=wiki_response[num_wiki], youtube_response=youtube_response[num_yt])
       
        except:
            return render_template("error.html")
    
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def application_error(e):
    return render_template('error.html'), 500