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
            response = response["nyt_api"]
            num = random.randint(0, len(response) - 1)
            return render_template("results.html", response=response[num])
        except:
            return render_template("error.html")
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def application_error(e):
    return render_template('error.html'), 500