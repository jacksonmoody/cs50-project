from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('youtube', 'v3', credentials=creds)
        request = service.search().list(
            part="snippet",
            maxResults=1,
            q="Jiminy Cricket",
            regionCode="US"
        )
        response = request.execute()
        title = response['items'][0]['snippet']['title']
        description = response['items'][0]['snippet']['description']
        thumbnail = response['items'][0]['snippet']['thumbnails']['high']['url']
        print(title)
        print(description)
        print(thumbnail)

        # A few ways we can take this: We can either embed the YouTube video into the website and have the title and description below it (thumbnail will automatically show). Otherwise, we could emb a link into the title/thumbnail and have a description below it and have the user redirect themselves to YT. Either works.
            # Embedding the video is easy and can be done with the <iframe> tag on HTML. We can just have a variable for the link and plug that variable into the iframe source parameter.
        # For randomization, we can think about potentially having the maxresults be higher and the number we index from the response be randomized. We could also have the keyword randomized as well --> both together will ensure significant randomization each time. 
        # Other parameters to think about adding to the search query are as follows: publishedAfter (can ensure we do not get some old video), topicId (broad topics we can ensure the search is in), videoDuration can give us videos at three lengths: long (>20 min), medium (4-20 min), and short (<4 min), videoSyndicated needs to be turned on if we want to emb the video into our website.
    except:
        print("Failed")

    

if __name__ == '__main__':
    main()