from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

advanced = "False"

@app.route("/", methods=["GET", "POST"])
def index():
    global advanced

    print(advanced)

    if request.method == "POST":

        category = request.form.get("category")
        advanced = request.form.get("advanced")

        if category == None or category == "" or advanced == "False":
            category_list = ['sports', 'technology', 'entertainment', 'science', 'politics']
            category = random.choice(category_list)

        match category:
            case "sports":
                background_image = "/static/images/sports.jpeg"
            case "technology":
                background_image = "/static/images/technology.jpeg"
            case "entertainment":
                background_image = "/static/images/entertainment.jpeg"
            case "science":
                background_image = "/static/images/science.jpeg"
            case "politics":
                background_image = "/static/images/politics.jpeg"
            case _:
                background_image = ""
                # Should never hit this case

        response = requests.get("https://cs50-project-backend.herokuapp.com/")
        response = response.json()
        print(response)

        try:
            nyt_response = response["nyt_api"][category]
            wiki_response = response["wiki_api"][category]
            youtube_response = response["youtube_api"][category]

            num_nyt = random.randint(0, len(nyt_response) - 1)
            num_wiki = random.randint(0, len(wiki_response) - 1)
            num_yt = random.randint(0, len(youtube_response) - 1)

            return render_template("results.html", category=category, advanced=advanced, background_image=background_image, nyt_response=nyt_response[num_nyt], wiki_response=wiki_response[num_wiki], youtube_response=youtube_response[num_yt])
       
        except Exception as e:
            print(e)
            return render_template("error.html")
    
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def application_error(e):
    print(e)
    return render_template('error.html'), 500