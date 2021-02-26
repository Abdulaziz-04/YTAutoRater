# Imports
# required : google-api-python-client,requests
from googleapiclient.discovery import build
# for OAuth
from google_auth_oauthlib.flow import InstalledAppFlow

# Setup API keys(for standard access) and Oauthkeys(for high level access)

# Setting Oauth key as client secret file via google console
# Download client oauth file from cloud console
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
# Setting the API KEY via google console
api_key = 'AIzaSyCES0pNKa7VZ5bV0WssiO-q2gVwbWdINaE'
# Channel ID can be retreived via url
# NEEDS TO BE CHANGED FOR PARTICULAR CHANNEL
channel_id = input('Enter the channel Id obtained via youtube URL ')

''' For Normal data analysis API KEY is sufficient'''
#youtube = build('youtube', 'v3', developerKey=api_key)
# Normal Search
#req = youtube.search().list(q='any query', part='snippet', type='channel' or 'video').execute()

# Setting up Oauth
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)
print(youtube)


def get_channel_videos(channel_id):
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    # Gettting all videos from the upload playlist
    upload_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    next_page_token = None
    while True:
        res = youtube.playlistItems().list(playlistId=upload_id, part='snippet',
                                           maxResults=50, pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        if(next_page_token is None):
            break
    return videos


# Performing operations on video
'''
LIMIT :10000
A read operation that retrieves a list of resources -- channels, videos, playlists -- usually costs 1 unit.
A write operation that creates, updates, or deletes a resource usually has costs 50 units.
A search request costs 100 units.
A video upload costs 1600 units.
'''

# For Inserting Comments


def insert_comment(youtube, channel_id, video_id, text):
    insert_result = youtube.commentThreads().insert(part='snippet', body=dict(
        snippet=dict(
            channelId=channel_id,
            videoId=video_id,
            topLevelComment=dict(
                snippet=dict(
                    textOriginal=text
                )
            )
        )
    )).execute()
    comment = insert_result['snippet']['topLevelComment']
    author = comment['snippet']['authorDisplayName']
    text = comment['snippet']['textDisplay']
    print(f'Author : {author}\nComment : {text}\n ')

# For liking/disliking Videos


def like_video(youtube, video, rate):
    youtube.videos().rate(
        rating=rate, id=video['snippet']['resourceId']['videoId']).execute()
    title = video['snippet']['title']
    print(f'Title : {title} \n rating : {rate} \n')


# Main Program
videos = get_channel_videos(channel_id)
for video in videos:
    like_video(youtube, video, 'like')
