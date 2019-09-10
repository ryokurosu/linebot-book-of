from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('RcIMrnirObeEFmUB1qe6BkJz9m/j2TGrXgKBF1F5LiOmN5DAfpAwBGuvw0oKMrMaffqW87e6DEduOdnRP0fGaAHch6RUFt/IfBlmSSsiuTlo2FnGKgbV2hkoFk5wP9x7WzA+EH3xl6468DORWN0mSAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('25e6e3b41f6c2c31de0ed49c9ae04fd4')

@app.route("/")
def index():
    return "Hello! Page!"

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
