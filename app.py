from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        response = requests.get("https://cs50-project-backend.herokuapp.com/")
        response = response.json()
        num = random.randint(0, 19)
        return render_template("results.html", response=response["nyt_api"]["results"][num]["url"])
    return render_template("index.html")