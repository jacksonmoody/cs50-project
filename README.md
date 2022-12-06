# CS 50 Final Project: The Random Interesting Thing Generator
By Abhay Duggirala, Minkai Li, and Jackson Moody

## Youtube Video 
<a href="http://www.youtube.com/watch?feature=player_embedded&v=iKeq4E1rrgs
" target="_blank"><img src="http://img.youtube.com/vi/iKeq4E1rrgs/0.jpg" 
alt="Video Project" border="10" /></a>

[https://youtu.be/iKeq4E1rrgs](https://youtu.be/iKeq4E1rrgs)

## Basic Setup
The Random Interesting Thing Generator randomly generates articles from The New York Times and Wikipedia as well as videos from YouTube. The website is easy to use once set up. Essentially, once a user has reached the home page, they can then click the main button to generate a random thing. Then, they will be directed to a results page with random articles and videos that fall under a certain category (entertainment, sports, politics, science, technology). The articles and videos have their title, description (not for Wikipedia), and a hyperlink to go to the website. Moreover, a YouTube video is embedded on the page. On that page, the user can either continue to find random things or can return home to engage in an “advanced search.” An advanced search allows the user to pick what category their random things will fall into. For example, if a user only wanted to see random things in science, they would click science in the dropdown of the advanced search and then search. Then, every time the user requests a random thing until they return home, they will get articles and videos in science. 

### Backend Setup
In the abstract, this application is broken down into two parts: the backend to query each API and return the relevant results and the frontend to display these results. Because the backend processes are quite time consuming (taking over a minute to run each time), we chose to host them asynchronously on Heroku. To configure Heroku, first navigate to https://id.heroku.com/login and create an account if you have not already. For simplicity purposes, we have already shared our pre-configured Heroku project with the teaching fellow grading the project. Thus, if the project has already been shared with you, simply click on “cs50-project-backend” in the Heroku dashboard (if it has not been shared, please email jacksonmoody@college.harvard.edu) . Then, navigate to the “resources” tab and click the pencil icon next to the `web gunicorn app:app --workers 1` Eco Dyno. Then, switch the Dyno from the off position to the on position and click “confirm”. This will initialize the backend process for the first time. From here, one can simply click “open app” to start the process running. To view the progress of the initialization, navigate to “more” in the top right hand corner and click “view logs.” Once the program outputs “Finished Updating” for the first time, backend is ready and the frontend application  is ready to be initialized. 

### Frontend Setup
As of now, this application was designed to be run locally on a computer. To ensure that you are ready to run it on your own computer, you must first install Python and the Pip package manager. To check if you have Python installed, execute `python --version` in a terminal window. If this returns a version number, you may proceed to the following steps. If it does not, you can download the latest version of Python from [python.org/downloads](python.org/downloads) and install it on your Mac or PC. 

If you installed Python using the above link, Pip should already be installed. To be sure, you can run the command `pip --version` in a terminal window. If Pip is not installed, run the command `python -m ensurepip --upgrade` to install it. 

Once you have both Python and Pip installed, you are ready to download and run the frontend application. To do so, navigate to https://github.com/jacksonmoody/cs50-project and click the green “Code” button in the upper right hand corner (if the GitHub repository has not been shared, please email jacksonmoody@college.harvard.edu) . Then click download ZIP and choose a suitable location on your computer. Once the file has downloaded, unzip the .ZIP file and navigate into the folder using `cd` commands in the terminal. 

Alternatively, if you already have access to the .ZIP file (via Gradescope or another medium), you can unzip it and run the code directly. However, this ZIP file will contain both the code for the frontend and the backend. Because the frontend is the only component of the application which is run locally, be sure that you are in the “frontend” folder before continuing. 
	
Once you are in the root folder, run `pip install -r requirements.txt` in the terminal to install the necessary Python packages. Once this completes, and the backend is running, you can run ‘flask run’ to initialize the front end application (if you have Python3 installed, run `python3 -m flask run`). This will generate a URL in the terminal window which will take you to the application once clicked. 

And that’s it! If both the frontend and backend are functioning properly, you should be able to use all of the application functionality. Once you are done, kindly reverse the steps from the backend section to turn off the Heroku app and help conserve running time costs. If you have any questions, please feel free to reach out to jacksonmoody@college.harvard.edu, aduggirala@college.harvard.edu, or minkaili@college.harvard.edu.  

## Advanced Setup
### Heroku
For simplicity’s sake, we have already configured Heroku and all of the necessary API keys. However, if any of the keys expire or if you would like to configure the application yourself, the following section will instruct you in how to do so. 

To configure Heroku for yourself, you will first need to create your own GitHub repository with all of the necessary code. To do so, you can fork the existing repository by navigating to https://github.com/jacksonmoody/cs50-project-backend and clicking “fork”—please email jacksonmoody@college.harvard.edu if you do not have access. (Alternatively, if you have access to a ZIP file of the code already, you can copy the code from the “backend” folder into a separate repository and initialize it using git). 

Once you have your own fork of the GitHub Repository, navigate to https://signup.heroku.com/ and create an account if you have not already. Then, create a new application at https://dashboard.heroku.com/new-app and follow the instructions to name the app, set a region, and add a payment method (you can ignore the pipeline step). 

Then, choose the “GitHub” deployment method and click the purple “Connect to GitHub” button. Authorize Heroku to access your GitHub account as appropriate, then paste “cs50-project-backend” (or the name of your GitHub fork if different) into the “repo-name” text box. Click “search,” then “connect” on the appropriate repository.  Lastly, click “deploy branch” to initialize the backend. As before, you can click “open app” in the top right hand corner to view the results, and navigate to “more” and “view logs” to track the progress of the initialization. Once the logs display “Finished Updating,” the backend has been configured! 

To configure the frontend to talk to the backend, take note of the url that appears when you click “open app” in Heroku. Copy this URL, and replace `BACKEND_URL` on line 7 of `app.py` in the frontend application repository with the result.

### API Keys
For simplicity, we have included the necessary API keys in the code already. However, if these keys expire or if you would like to create your own, follow the following instructions (Wikipedia does not have a key): 

##### New York Times
This setup is quite simple. Here, you will simply go to https://developer.nytimes.com/, and then sign up for an account (you will likely need a Times account associated with the email you use). Then, click the “Get Started” link and create an account with the website.  From there, you can sign into the Developer Portal. Click the drop down menu at the top of the website and go to your account at the bottom and click “Apps.” Then, click “New App.” Give your app a name and a description and enable one API: “Article Search API.” Then click save. You will then get a key which you can copy. You will then copy this key into the app.py file in the backend code at the part that says `NYT_KEY` in line 15.  Then, you are finished and can test the NYT API with your own key! Keep in mind that this key can only be requested 10 times per minute and 4,000 times per day (hence, the time.sleep commands that we have in our code).

##### YouTube
This setup is a little bit more involved and required some macgyvering in order to work with Heroku and our app the way that we have it. First, you will need to console.cloud.google.com and sign into your desired Google account. From there, you will agree to any terms and conditions and set your country as the United States. Then, there should be a button called select a project at the top of the “Get Started Page.” Once you click that button, click “New Project.” You can name this project whatever you want and get it affiliated with some parent organization or folder if you would like. Once this project is created, select it. On the main dashboard, click “Go to APIs overview.” Then, at the top of that dashboard, click the blue “Enable APIs and Services” button. In the search bar, search for “YouTube” and click on the “YouTube Data API v3” result. Enable this API. Then, on the page that it redirects you to, click “Create Credentials” at the top. Then, when it asks for credential type, click “User data.” Then, fill in the App information, your email address as the user support and developer email, and continue. On step 3, you will need to add a scope. The scope you will need to add is as follows: “YouTube Data API v3” with the scope that says “/auth/youtube.readonly.” Then, save this scope and proceed to step 4. Make sure that the application type is “Web application” and you can name the web client whatever you want. Then, you will need to add a URI for the Authorized JavaScript origins page. Plug in this URI “https://localhost” (without the quotes). Then, plug in this authorized redirect URIs “https://developers.google.com/oauthplayground” (without the quotes). 

If your Google account is with an organization, ignore this step. If it is not, then go to the OAuth Consent Screen under the APIs and Services Dashboard. Then, click “Add Users” and add your own email. 

Now, go to this link https://developers.google.com/oauthplayground. Then, click the gear in the top right and check the box that says “Use your own OAuth credentials.” Then, go back to the Google Cloud and go to the “Credentials” page under “API and Services.” Click on the OAuth 2.0 Client ID that you just made. On the right side of the screen will be the “Client ID” and “Client secret.” Copy these and place them into the corresponding boxes in the OAuth playground website. Then, close that menu and go to menu on the left and authorize the “YouTube Data API v3 v3” and click the link that has “https://www.googleapis.com/auth/youtube.readonly.” Then, sign in with the Google account that you have been using and continue. Then, click “exchange authorization code for tokens.” Then, note down the Refresh token. Now, we must go back into our own backend code and switch a few keys. At the top of the backend app.py code, switch the `API_REFRESH TOKEN`, `CLIENT_ID`, and `CLIENT_SECRET` (lines 11-13) with the corresponding codes that we just got. Then, we are finished with the YouTube API!

## Final Notes
Finally, a few things to keep in mind are as follows:

When specific interesting things that come up do not fit with the category, have an image that is poor, or might be in a different language, this is generally the fault of the API we are using. There are YouTube videos that are miscategorized by region/language as well as topic as well as some New York Times Articles that are miscategorized by topic. 

Our YouTube API has the search filter `videoSyndicated=true` meaning that all of our videos should theoretically be able to be played outside of youtube.com. However, this is not always the case because of issues on YouTube’s end and thus there are some moments where a video is unplayable on our website and must be played on youtube.com still.


