from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        category = request.form.get("category")

        if category == None or category == "":
            category_list = ['sports', 'art', 'technology', 'business', 'entertainment', 'science', 'health', 'politics']
            category = random.choice(category_list)

        match category:
            case "sports":
                background_image = "https://thumbs.dreamstime.com/b/sports-seamless-pattern-25616314.jpg"
            case "art":
                background_image = "https://img.freepik.com/premium-vector/vector-black-white-floral-seamless-pattern-hand-drawn-line-simple-trendy-illustration-with-flowers-leaves-bohemian-repeating-background-with-plants-boho-digital-paper-coloring-pagexa_150240-2514.jpg?w=2000"
            case "technology":
                background_image = "https://thumbs.dreamstime.com/b/vector-technology-pattern-technology-seamless-background-vector-technology-pattern-technology-seamless-background-vector-123145077.jpg"
            case "business":
                background_image = "https://img.freepik.com/premium-vector/business-themed-seamless-background_6997-976.jpg"
            case "entertainment":
                background_image = "https://media.istockphoto.com/id/968278390/vector/arts-and-entertainment-seamless-background.jpg?s=612x612&w=0&k=20&c=2JwZcif0eDzkf98N8TaBdS9s_dNqbRsgS_rdFnH9oNI="
            case "science":
                backbround_image = "https://www.philipgordts.com/wp-content/uploads/2018/03/seamless-science-background-vector-3740137.jpeg"
            case "politics":
                background_image = "https://img.freepik.com/premium-vector/vector-flat-seamless-texture-pattern-democracy-political_51635-1282.jpg"
            case _:
                background_image = ""
                # Should never hit this case

        response = requests.get("https://cs50-project-backend.herokuapp.com/")
        response = response.json()

        try:
            nyt_response = response["nyt_api"]
            wiki_response = response["wiki_api"]
            youtube_response = response["youtube_api"]

            num_nyt = random.randint(0, len(nyt_response) - 1)
            num_wiki = random.randint(0, len(wiki_response) - 1)
            num_yt = random.randint(0, len(youtube_response) - 1)

            return render_template("results.html", category=category, background_image=background_image, nyt_response=nyt_response[num_nyt], wiki_response=wiki_response[num_wiki], youtube_response=youtube_response[num_yt])
       
        except:
            return render_template("error.html")
    
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def application_error(e):
    return render_template('error.html'), 500