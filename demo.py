import json
import os
import datetime
import re
import pandas as pd #엑셀 형태로 저장하기 위한 라이브러리
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient import discovery
import json
from urllib.parse import urlparse, parse_qs
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




def video2excel(video_id):

    DEVELOPER_KEY = 'AIzaSyBswrX1sQBFfVbbpLQGAeMWuT6DwxSnQiY'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    # Path to the json file you downloaded:
    # path_json = 'rest.json'

    # with open(path_json, encoding='UTF-8') as f:
    #     yt = json.load(f)

    # service = discovery.build_from_document(yt, developerKey=DEVELOPER_KEY)

    service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY, static_discovery=False)

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
        thumbnail = rs['thumbnails']['standard']['url'] if 'standard' in rs['thumbnails'] else rs['thumbnails']['high']['url']
        channel_name =rs['channelTitle']
        publish_date = rs['publishedAt'][:-1]
        view_count = st['viewCount']
        comment_count = st['commentCount']
        like_count = st['likeCount']

        row.append([video_url, video_title, publish_date, channel_name, view_count, comment_count, like_count, video_desc, thumbnail])
        df = pd.DataFrame(data=row, columns=columns)
        

        if os.path.isfile("youtube.xlsx"):
            df2 = pd.read_excel("youtube.xlsx")
            df= pd.concat([df2,df], axis=0)
        
        df.to_excel("youtube.xlsx", index=False)
        print("File Success")
        return response['id']



# https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        print(query.path[1:])
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            print(p['v'][0])
            return p['v'][0]
        if query.path[:7] == '/embed/':
            print(query.path.split('/')[2])
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            print( query.path.split('/')[2])
            return query.path.split('/')[2]
    # fail?
    return None


# if __name__ == "__main__":    
#     while True:
#         url = input("url 입력 = ")
#         id = video_id(url)
#         video2excel(id) 