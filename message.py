from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

line_bot_api = LineBotApi(os.environ.get("ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_ID"))

debug_line_bot_api = LineBotApi(os.environ.get("DEBUG_ACCESS_TOKEN"))

app_env = ""
if os.environ.get("APP_ENV"):
	app_env = os.environ.get("APP_ENV")
else:
	app_env = "本番用"

def send_group_message(group_id,message_text):
    line_bot_api.push_message(
        group_id,
        TextSendMessage(text=message_text))

def send_all_message(message_text):
    line_bot_api.broadcast(TextSendMessage(text=message_text))

def send_debug_message(message_text):
	message_text = app_env + "\n" + message_text
	debug_line_bot_api.broadcast(TextSendMessage(text=message_text))

if __name__ == "__main__":
    send_all_message('hello')