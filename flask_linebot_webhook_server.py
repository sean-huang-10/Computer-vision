from flask import (
    Flask, 
    request, 
    abort, 
    render_template
)
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
    TextMessage  # 傳輸回Line官方後台的資料格式
)
from linebot.v3.webhooks import (
    MessageEvent, # 傳輸過來的方法
    TextMessageContent # 使用者傳過來的資料格式
)
from handle_keys import get_secret_and_token
from openai_api import chat_with_chatgpt
import os,sys
app = Flask(__name__)

def get_secret_and_token():
    # 1. 先到Line Developer Console，把 Channel Secret & Channel Access Token複製起來
# 2. 把這兩個密文，存到環境變數內；工具列搜尋<環境變數>，新增兩個環境變數，並且把值貼上去
# 3. 按下確定儲存，要記得你的變數名稱，這些資訊只會存在你當前使用的電腦裡。
# 4. 透過以下程式碼，取得環境變數儲存的對應數值。
    channel_secret = os.getenv('LINEBOT_SECRET_KEY', None)
    channel_access_token = os.getenv('LINEBOT_ACCESS_TOKEN', None)
    if channel_secret is None:
        print('Specify LINEBOT_SECRET_KEY as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        print('Specify LINEBOT_ACCESS_TOKEN as environment variable.')
        sys.exit(1)
    return {
        'LINEBOT_SECRET_KEY':channel_secret,
        'LINEBOT_ACCESS_TOKEN':channel_access_token
    }
keys = get_secret_and_token()
handler = WebhookHandler(keys['LINEBOT_SECRET_KEY'])
configuration = Configuration(access_token=keys['LINEBOT_ACCESS_TOKEN'])

@app.route("/")
def say_hello_world(username=""):
    # 測試用，確定webhook server 有連通
# 設計一個 #callback 的路由，提供給Line官方後台去呼叫
# 也就所謂的呼叫Webhook Server
# 因為官方會把使用者傳輸的訊息轉傳給Webhook Server
# 所以會使用 RESTful API 的 POST 方法
    return render_template("hello.html", name=username)

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
    # 根據不同的使用者事件(event)，用不同的方式回應
# eg. MessageEvent 代表使用者單純傳訊息的事件
# TextMessageContent 代表使用者傳輸的訊息內容是文字
# 符合兩個條件的事件，會被handle_message 所處理
    user_message = event.message.text #使用者傳的訊息
    api_key = os.getenv("OPENAI_API_KEY", None)
    response = chat_with_chatgpt(user_message, api_key )

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=response)
                ]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)