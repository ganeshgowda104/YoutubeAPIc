import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
api_key = os.environ.get("YT_API_KEY")

credentials = None



if os.path.exists('token2.pickle'):
    print('Loading Credentials From File.....')
    with open('token2.pickle', 'rb') as token:
        credentials = pickle.load(token)

# if there are no valid credentials available, then either refresh the token or log in
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json",
            scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]  # Update the scope
        )

        flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message='')

        credentials = flow.credentials

        # Save the credentials for the next run
        with open("token2.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

youtube = build("youtube", "v3", credentials=credentials)

with open('lang.txt', 'r') as file:
    # Read the content of the file
    content = file.read()

    # Split the content by commas to get individual names
    names_list = content.split(',')

    # Remove leading and trailing whitespaces from each name
    names_list = [name.strip().strip('"').lower() for name in names_list]

for name in names_list:
    search_query = name + " best songs"

    # Make a request to the API to search for videos
    search_response = youtube.search().list(
        q=search_query,
        part='id,snippet',
        type='video',
        order='viewCount',
        maxResults=1
    ).execute()

    # Extract information from the search results
    videos = []
    for search_result in search_response.get('items', []):
        video = {
            'title': search_result['snippet']['title'],
            'video_id': search_result['id']['videoId'],
            'thumbnail_url': search_result['snippet']['thumbnails']['default']['url']
        }
        videos.append(video)

    # Print or use the extracted information
    for video in videos:
        vid_id = video['video_id']
        request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': 'PLHQp3p8VQN1CyG0Kw-oTNERpjSyEw2G8B',  # Replace with your playlist ID
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': vid_id,
                    }
                }
            }
        )
        response = request.execute()
        print(f"Video {vid_id} added to the playlist.")