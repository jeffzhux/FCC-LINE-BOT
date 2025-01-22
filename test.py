from googleapiclient.discovery import build
from datetime import datetime
today = datetime.now()

DEVELOPER_KEY='AIzaSyBKrXe6N_46-7XcLXKFzwQAK9-3HVSKx8c'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

request = youtube.search().list(
    part="snippet",   
    q=f"[活潑的生命]{today.year}{today.month:02d}{today.day:02d} 主所賜的真是可吃和可喝的",
    maxResults=50
)
response = request.execute()
print(response,"\n")
print(f"[活潑的生命]{today.year}{today.month:02d}{today.day:02d} 主所賜的真是可吃和可喝的")
for i in response['items']:
    
    id = i['id']['videoId'] if 'videoId' in i['id'] else ''
    title = i['snippet']['title'] if 'title' in i['snippet'] else ''
    if f'{today.year}{today.month:02d}{today.day:02d}' in title:
        print(f'-----------https://www.youtube.com/watch?v={id}')
    print(id)
    print(title)
    

#print(response,"\n")