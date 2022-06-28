import json
import os
import datetime
import re
from matplotlib.image import thumbnail
import pandas as pd #엑셀 형태로 저장하기 위한 라이브러리
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import json
from pprint import pprint

#service => connetion to youtube data api
def get_video(service, video_id):
    try:
        response = service.videos().list(
            part="id, snippet, statistics", #응답 받을 내용들
            id = video_id

        ).execute()

        return response['items']
         
    except HttpError as e:
        errMsg = json.loads(e.content)
        print('HTTP Error:')
        print(errMsg['error']['message'])



# #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# CLIENT_SECRETS_FILE = "client_secrets.json"

# # This OAuth 2.0 access scope allows for full read/write access to the
# # authenticated user's account.
# SCOPES = ["https://www.googleapis.com/auth/youtube"]
# API_NAME = "youtube"
# API_VERSION = "v3"    
def main():
    DEVELOPER_KEY = "AIzaSyDqMOpJralVVgKQSRsnpHrl6L6v2Qatzjc"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    video_id = "n1Fs9wxw8ro"

    video = get_video(service, video_id)

    response = video[0]

    if response:
        row=[]
        columns = ['Video Link', 'Video Title', 'Publish Date',  'Channel Name', 'Views', 'Comments','Likes','Description', 'Thumbnail' ]
        rs = response['snippet']
        st = response['statistics']

        video_url = "https://www.youtube.com/watch?v={0}".format(response['id'])
        video_title = rs['title']
        video_desc = rs['description']
        thumbnail = rs['thumbnails']['standard']['url']
        channel_name =rs['channelTitle']
        publish_date = rs['publishedAt'][:-1]
        view_count = st['viewCount']
        comment_count = st['commentCount']
        like_count = st['likeCount']

        row.append([video_url, video_title, publish_date, channel_name, view_count, comment_count, like_count, video_desc, thumbnail])
        df = pd.DataFrame(data=row, columns=columns)

        if os.path.isfile("youtube.xlsx"):
            df2 = pd.read_excel("youtube.xlsx")
            df2.append(df)

        df.to_excel("youtube.xlsx")




if __name__ == "__main__":
    main() 