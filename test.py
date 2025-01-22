from googleapiclient.discovery import build
from datetime import datetime
today = datetime.now()


def get_youtubeId(date, title):
    DEVELOPER_KEY='AIzaSyBKrXe6N_46-7XcLXKFzwQAK9-3HVSKx8c'
    youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
    request = youtube.search().list(
        part="snippet",   
        q=f"[活潑的生命]{date} {title}",
        maxResults=50
    )
    response = request.execute()

    for i in response['items']:
        id = i['id']['videoId'] if 'videoId' in i['id'] else ''
        title = i['snippet']['title'] if 'title' in i['snippet'] else ''
        print(id)
        print(title)
        if date in title:
            return f'https://www.youtube.com/watch?v={id}'
    return ''
date = f'{today.year}{today.month:02d}{today.day:02d}'
topic = '主所賜的真是可吃和可喝的'
print(get_youtubeId(date, topic))