# Design Document
## Backend
On the backend, we split the work into three main functions, nytapi, wikiapi, and youtubeapi. This is because each of the APIs was fundamentally different and it would have been incredibly difficult, if not impossible, to try to search all of them in a generalized process. 

Next, each of the api functions accepts one of five categories (sports, politics, entertainment, technology, and science). This was done for a few reasons. First, it allowed us to create a more unified theme among the Wikipedia, NYT, and Youtube links that we ultimately show the user (and change the front end banner and title depending on what that theme is). Second, it allows us to provide the option for the user to pick a specific category. Third, it provides us an ability in the future to potentially adapt the site and implement an algorithm that adopts the content it shows the user based on which categories the user liked/disliked or clicked on/didn’t click on (by showing some categories more and others less). Each function appends a list of articles within the passed in category to our result dictionary which we use as the “database” that our frontend pulls from whenever the user wants to generate an article.

Within each of those five categories, we had to hardcode in subcategories. This is because the APIs didn’t have a way for us to generally search for a category. For example, we couldn’t generally search in Wikipedia for sports articles or articles about technology. Thus, we found other ways to query into each of the API’s and then adapted these for our categories. For example, for the Wikipedia API, to find articles on science, we would find pages listed in the categories of Climate change, Nature Conservation, Pollution, and other similar categories. Other APIs like Youtube and New York Times had specific lists of topics we could query which we then hard coded into our specific categories.

However, there were certain limitations of the APIs that we had to work around—a fact most evident in our nytapi function. First, the NYT’s API will only ever return 10 articles for any given query. This posed a problem for us because when we searched within a given subcategory, the API would always return the same 10 articles (this is notably different than Youtube which returns a different assortment of videos every time and less of an issue with Wikipedia as each query can return far more articles); this could create a bad user experience (for example, if the user happens to come onto the site two different times and the subcategory that was randomly selected within a specific category was the same, they would see a repeat of the same 10 articles). To work around this, we first query the NYT for a specific subcategory and see how many “hits” it has (articles in that subcategory). By default, the NYT’s API returns the first page of results (where each page consists of 10 articles). We change that behavior by picking a random page (the page query only will accept a positive integer up to 100, which is why we take the minimum of the true number of pages and 100). We then requery into the API with a random page number to add more variety into the articles we provide for the user. Moreover, one can only query into the NYT’s API 10 times every minute, so the New York Time’s asks that you wait six seconds between queries. To account for this, we added time.sleep(6) in both the mainapi() and the nytapi() functions. We ran two queries instead of hardcoding the page counts for each topic so that our code is more dynamic.

With Wikipedia’s API, we query it as follows. First, we query for the category members of a category (these are the pages and subcategories at the bottom of a category). Then, to only get the pages and not another category, we only add titles that do not have “Category” in the title to our results list (all category pages have “Category” in the title). We can simply append the title of the article to the home URL of Wikipedia to get the link to the article (we do this because Wikipedia’s API does not return URLs). 

To run the YouTube API, we must first authenticate using the OAuth2.0 flow in accordance with Google’s specification. In general, this process requires getting a refresh token using a particular “client id” and “client secret,” and then using this refresh token to obtain a temporary token to use with Bearer authentication in all future API requests. To simplify this process, and knowing that our application would not be running long enough to require re-authentication (generally a period of about 6 months), we chose to use Google’s OAuth Playground (as outlined in README.md) to generate the refresh token. Then, every time the backend application initializes, it uses this refresh token to generate a bearer token to be used in all future API requests. Unfortunately, YouTube requirements state that you can only run a maximum of 100 queries a day under their free, unverified plan. Therefore, we are currently only able to request every 10 minutes to avoid reaching this quota in too short a time period (as of now, the application can still only run for about two hours using one API key). If we had more flexibility with this, we might run the API’s more often to ensure the user always gets random articles even if they request more videos an excessive amount of times.  
	
Some other design decisions that we made are as follows:
1. For the New York Times, some articles did not have an image, so we added a default image if the article did not have one. 
2. For the Youtube and NYT APIs, we check if the description has a link and if it does, we delete the entry. This is because links have trouble formatting in our frontend html (`<a href=...` messes with our code). 
3. Since YouTube still does not always give us English videos when we have set the language to English and the regionCode to the United States, we ensure that the title of each video is in English as another filter to stop us from getting videos in foreign languages. 
4. Since YouTube has problematic html values in its titles (ex. &lt representing “<”), we decode each title and description using a function that replaces these values with their corresponding symbol.
5. Lastly, since our Wikipedia links are made by appending the title of the page to the link, we have to add underscores to any title that has a space in it so our links are formatted the way Wikipedia formats them. We do this using a helper function.
	
Another key design decision that we made was choosing to employ global variables to store the results from the New York Times, YouTube, and Wikipedia APIs. Although using global variables is generally something worth avoiding, we chose to use them to maintain the uptime of our API. That is, we needed the mainapi() function to be able to run every 10 minutes to update the database. At the same time, anytime the frontend pinged the backend, the backend needed to return the most recently updated version of the API results. Because multiple functions (the one run every 10 minutes to update and the one run when the frontend pings the backend) needed to read and modify the nyt_result, youtube_result, and wiki_result variables, employing global variables seemed to be the optimal design choice. 

For more specificity on how the results from the APIs were being stored, note that the main idea was that each of the nytapi, youtubeapi, and wikiapi functions were ultimately editing each global dictionary (nyt_result, youtube_result, and wiki_result). That dictionary has a key for each of our 5 categories and the value associated with that key is a list of dictionaries. Within that list, each dictionary ultimately holds the information we wanted to draw from a specific article/video (for example, for a Youtube video we want its title, URL, and description). These dictionaries give us the flexibility to ultimately request a certain category of articles/videos if a user uses our advanced search function to search for links within a specific category and to also ensure our videos and articles are matched in a certain category.

The reason we did everything on a backend using Heroku was for speed and to save computing power on local machines. Essentially, we did not want there to be a situation where every time a user clicked “generate interesting thing” (or every time they visited the website) they would have to wait the entire minute or so for our queries to run. Since our APIs are limited in how fast and how often we can query them, it was simply a better design decision to have everything running on a backend so a user could quickly generate interesting things without having to requery and wait. Moreover, since we are querying so many different APIs and sorting through them, it saves the local machine a lot of computing power and makes our program run more smoothly for anyone who chooses to set it up. We also do not have to requery based on the category filter that a person puts in the advanced search as we always have a database of articles and videos from all categories to draw from (which refreshes/randomizes every few minutes). 

Finally, on the backend, we return a JSON file to the frontend when it is requested. We then use APScheduler to run the function after every specified interval of 10 minutes so we are constantly refreshing/randomizing the articles/videos on the backend without any input from the user.

## Frontend

We primarily used Flask, Python, HTML, and CSS to run the frontend of our website. The way we set this up was fairly similar to CS50 Finance where we had an app.py file that ran our code, Jinja in our HTML code that allowed us to pass in data from the backend, and CSS/HTML to style and build our website. We have error pages for 404 and 500 errors which were helpful when we debugged and when there are errors in the website. 

The app.py file essentially works as follows. First, we check if the user submitted a post request (which would have occurred if they had clicked the button on the home page to either search or advanced search). If they did, then we get the category and advanced values from the website (they are none and False if the user did not advance search and are the name of the category and True if the user did advanced search and put in a category). If the user did not use advanced search, we choose a random category for the user ourselves. Then, we simply match the category name to a corresponding category image which we will use as the header image for the results page. From there, we simply request the backend for the JSON file with all of our data and then get each of the corresponding results for the category that we are searching for. Then, we get a random number that is between 0 and the length of the response (number of articles/videos) minus one to add even more randomness (by providing us with a random article/video from our response). Then, we pass in all of the articles/videos into our results template which we formatted with Jinja.

To implement our advanced search functionality, we also store the status of the category and advanced variables in the same function. Advanced is a boolean variable that indicates whether or not the user specified a category or if a category needs to be randomly chosen. If it is True, then the user already specified a category which is stored. However, if it is False, then the program randomly selects a category for the user. Both of these variables are sent in the post requests from either the homepage or the results page—thereby ensuring that users who specified a category via the advanced search continue searching that category when they click “next” on the results page and that users who did not are shown a random category each time when they click “next.”

## Mobile Design Caveat

We unfortunately realized too late that our website was not optimized for mobile devices. While the site already has the viewport set to the device width to control  the scaling of the website on different devices, we could make further improvements (if given more time) to rescale and restructure certain HTML and CSS elements. 

For one, we could employ media queries in our CSS code to only apply certain CSS styling for certain device sizes. In an ideal world, we would likely have four media queries: `@mediaonly screen and (max-width: 600px)` for small mobile devices, `@media only screen and (min-width: 600px)` for larger mobile devices, `@media only screen and (min-width: 768px)` for tablets, and `@media only screen and (min-width: 992px)` for desktop devices. Under each respective media query, we would then adjust the font sizes and margins accordingly (with larger margins/font sizes corresponding to larger screen sizes and vice versa). 

Secondly, we could restructure our HTML table on the results.html page for smaller screen sizes to use only one column instead of two. That way, all of the information would be more easily accessible as the user scrolls vertically (rather than requiring them to scroll horizontally). 

Unfortunately, both of these improvements would be rather difficult to implement given the short time frame of this project (as both would require modifying much of the HTML/CSS for different screen sizes). Given more time, however, this would certainly be an area upon which we would like to improve.
	
# Please enjoy our project! 