from googleapiclient.discovery import build
from datetime import datetime

youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
today = datetime.now()
request = youtube.search().list(
    part="snippet",   
    q=f"活潑的生命{today.year}{today.month}{today.day}"
)
response = request.execute()
for i in response['items']:
    id = i['id']['videoId']
    title = i['snippet']['title']
    print(id)
    print(title)
    break

print(response,"\n")