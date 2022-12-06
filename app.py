from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

BACKEND_URL = "https://cs50-project-backend.herokuapp.com/"

@app.route("/", methods=["GET", "POST"])
def index():
    # We need to declare advanced here to future use, so we set it equal to nothing to begin with.
    advanced = ""

    # If the user selects either of the search (advanced or not) buttons, we will run the code below.
    if request.method == "POST":

        # We get the category and advanced values from the form (advanced is true if they submit the advanced search form, false if they go through the regular search)
        category = request.form.get("category")
        advanced = request.form.get("advanced")

        # If the user does not select a category and submit the advanced search, a random category will be selected
        if category == None or category == "" or advanced == "False":
            category_list = ['sports', 'technology', 'entertainment', 'science', 'politics']
            category = random.choice(category_list)

        # Selecting the background/header image for the results page
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

        # Here, we request the backend to get our database of articles
        response = requests.get(BACKEND_URL)
        response = response.json()

        try:
            # Selecting the respective lists that contain the article/video information for a specified category (either the one the user picked or the random one we picked)
            nyt_response = response["nyt_api"][category]
            wiki_response = response["wiki_api"][category]
            youtube_response = response["youtube_api"][category]

            # Selecting a random entry (article or video) from those lists
            num_nyt = random.randint(0, len(nyt_response) - 1)
            num_wiki = random.randint(0, len(wiki_response) - 1)
            num_yt = random.randint(0, len(youtube_response) - 1)
            # Returning all of the data to the results page (articles and videos and images) to be used.
            return render_template("results.html", category=category, advanced=advanced, background_image=background_image, nyt_response=nyt_response[num_nyt], wiki_response=wiki_response[num_wiki], youtube_response=youtube_response[num_yt])
       
       # This helps us know what the error message is if our code breaks.
        except Exception as e:
            print(e)
            return render_template("error.html")
    
    # Return homepage if we never had a POST request.
    return render_template("index.html")

# We bring up error pages for 404 and 500 errors that may come up when running the program.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def application_error(e):
    print(e)
    return render_template('error.html'), 500