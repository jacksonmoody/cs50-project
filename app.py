from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        response = requests.get("https://cs50-project-backend.herokuapp.com/")
        response = response.json()
        return render_template("results.html", response=response["message"])
    return render_template("index.html")