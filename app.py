from flask import Flask, request, abort
from apscheduler.schedulers.background import BackgroundScheduler
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

def scrapy_text():
    re = requests.get('https://www.duranno.tw/livinglife/index.php/daily')
    soup = BeautifulSoup(re.text,"html.parser")

    today = datetime.now()
    topic = soup.find("h2")
    topic = str(topic).replace('\n','').replace(' ','')[4:-5].replace('<br/>',' ')

    verse = soup.find("div", {"class": "range"}).get_text()
    verse = verse.replace('\n','').replace(' ','')

    message = f'''弟兄姊妹平安，你今天QT了嗎?
    讓我們每天用《活潑的聖命》一起QT
    《{today.year}年{today.month}月{today.day}日》
    【QT主題:{topic}】
    【QT經文進度:{verse}】'''
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
scheduler = BackgroundScheduler()
scheduler.start
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