from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://cs50-project-backend.herokuapp.com/")
    response = response.json()
    return render_template("index.html", response=response["message"])