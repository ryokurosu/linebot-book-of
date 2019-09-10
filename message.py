from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('RcIMrnirObeEFmUB1qe6BkJz9m/j2TGrXgKBF1F5LiOmN5DAfpAwBGuvw0oKMrMaffqW87e6DEduOdnRP0fGaAHch6RUFt/IfBlmSSsiuTlo2FnGKgbV2hkoFk5wP9x7WzA+EH3xl6468DORWN0mSAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('25e6e3b41f6c2c31de0ed49c9ae04fd4')

def send_group_message(group_id,message_text):
    line_bot_api.push_message(
        group_id,
        TextSendMessage(text=message_text))

if __name__ == "__main__":
    group_id = "C470f005f930f761475f92fb0ed5bab8e"
    send_group_message(group_id,'hello')