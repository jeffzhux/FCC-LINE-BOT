from flask import Flask, request, abort
from apscheduler.schedulers.background import BackgroundScheduler
from googleapiclient.discovery import build

import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

def get_youtubeId(date, title):
    DEVELOPER_KEY=''
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

        if date in title:
            return f'https://www.youtube.com/watch?v={id}'
    return ''


def scrapy_text():
    re = requests.get('https://www.duranno.tw/livinglife/index.php/daily_p')
    soup = BeautifulSoup(re.text,"html.parser")

    today = datetime.now()
    topic = soup.find("h2")
    topic = str(topic).replace('\n','').replace(' ','')[4:-5].replace('<br/>',' ')

    verse = soup.find("div", {"class": "range"}).get_text()
    verse = verse.replace('\n','').replace(' ','')

    url = get_youtubeId(f'{today.year}{today.month:02d}{today.day:02d}', topic)
    print(f'{today.year}{today.month:02d}{today.day:02d}', topic)
    message = (
        f'''弟兄姊妹平安，你今天QT了嗎?\n'''
        f'''讓我們每天用《活潑的聖命》一起QT\n'''
        f'''《{today.year}年{today.month}月{today.day}日》\n'''
        f'''【QT主題:{topic}】\n'''
        f'''【QT經文進度:{verse}】\n'''
        f'''【推薦影片:】{url}'''
        )
    
    return message

def quit_time():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


app = Flask(__name__)

configuration = Configuration(access_token=os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print(event.message.text)
    if '聖經' != event.message.text:
        return
    message = scrapy_text()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=message)]
            )
        )

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(quit_time, 'cron', hour=6)
    scheduler.start()
    app.run(host='0.0.0.0', port=10000)