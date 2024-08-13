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
from cwa_opendata_scraper import get_cities_weather

app = Flask(__name__)
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
    user_id = event.source.user_id  #使用者id
   # print("User ID",user_id)
    user_message = event.message.text #使用者傳的訊息{"destination":"Uc474244ed30fb68a4a346524b727e811","events":[{"type":"message","message":{"type":"text","id":"521097010611749041","quoteToken":"UMQ2xwhuefnKBNM5KpYA9Ku76ehiAqzvpguZvvJOtv_69nPiliF_5ezwyyFNTvEsZZo5fRLiOVt98ERKqk-NRQ4T2sa837H-tknc9IgRa9tjPb2oR_6Bq8JgI_GSlIY_-4OpQUXlytOUxWN5376wHw","text":"超愛"},"webhookEventId":"01J52693KKQ6FSAKDKC7Q2M4GM","deliveryContext":{"isRedelivery":false},"timestamp":1723429326120,"source":{"type":"user","userId":"U897c15e0aace9a1f6e76d073b899461a"},"replyToken":"6d5fd1be9b384eb9b4a3617a80326e13","mode":"active"}]}
    api_key = keys["OPENAI_API_KEY"]
    
    #假定的格式: 天氣如何 臺中市 桃園市 彰化市
    if '天氣如何' in user_message:
        #問天氣
        cwa_api_key = keys['CWA_API_KEY']
        locations_name = user_message.split()[1:]
        if locations_name: #有地點才做事
            weather_data = get_cities_weather(cwa_api_key, locations_name)
            
            response = ""
            for location in weather_data:  #取得每一個縣市的名稱
                response += f"{location} :\n" #加入縣市名稱訊息到response
                for weather_key in  sorted(weather_data[location]): #根據縣市名稱，取得縣市天氣資料
                    response += f"{weather_key}:{weather_data[location][weather_key]}\n" 
            response = response.strip()
            response = chat_with_chatgpt(
                user_id ,response, api_key, 
                extra_prompt="請你幫我生出一段報導，根據前面的天氣資訊，建議使用者穿搭等等，每個縣市分段，200字以內" )
        #台中市:
        #       xxx:aaa
        #       yyy:bbb
        #       zzz:ccc
        else:    
        #閒聊
            response = "請給我你想知道的縣市，請輸入:天氣如何 臺中市 桃園市 彰化市"
    else:
        # 閒聊
        response = chat_with_chatgpt(user_id, user_message, api_key)
    
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