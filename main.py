from fastapi import FastAPI , HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.gemini import Gemini
#from api.test import fetch_and_save_news_as_json
#from api.get_news import scrape_news

import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent

# 要抓取的新闻网页
url = "https://www.ettoday.net/news/news-list.htm"
url_fornews = "https://www.ettoday.net/news/"

def fetch_url_with_retry(url, headers):
    return requests.get(url, headers=headers)
# 抓取新闻标题和链接的函数，限制只抓取前5则
def scrape_news():
    #變換ua
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    
    try:
        response = fetch_url_with_retry(url, headers=headers)
        #print("第一次就成功", formatted_time)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        response.raise_for_status()
        #print(f"Error fetching URL: {e}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='part_list_2')
        for i, item in enumerate(news_items[:5]):
            title = item.find('h3').text
            relative_link = item.find('a')['href']
            full_link = urljoin(url_fornews, relative_link)  # 将相对链接转换为完整链接
            message = f"隨選新聞: {title}\n網址: {full_link}"
    return message

import os

app = FastAPI()
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
gemini = Gemini()


@app.post("/webhook")
async def callback(request:Request):
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = await request.body()
    # handle webhook body
    try:
        line_handler.handle(body.decode(), signature)
    except:
        print(body, signature)
        raise HTTPException(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_id = event.source.user_id  # 取得用戶的 user_id
    print(f"User ID: {user_id}")  # 打印用戶 ID（可以用來 debug）
    
    allowed_user_ids = [
        "U34651e48067cdde9fb6df533b53e367c",
        "U092b3fc3dcef603a0fc0a56000468e1d",
        "U14f71a8ff59d964b579a047c6367a0e3",
        "U12c2b60e458a682b63ad793e325613df",
        "U8c73d74ccc1d8e059579dff534ee5944",
        "U71e913efad74b8a08fec3abe77afaa84",
        "U3807500678de3139b65b5e29fc60021d"
    ]  # 允許的 user_id 清單
    #U34651e48067cdde9fb6df533b53e367c 隆
    #U092b3fc3dcef603a0fc0a56000468e1d 不路
    #U8c73d74ccc1d8e059579dff534ee5944 印節
    #U71e913efad74b8a08fec3abe77afaa84 nono
    #U3807500678de3139b65b5e29fc60021d pa2
    if event.source.user_id not in allowed_user_ids:
        # 如果用戶不在允許清單中，回應一個提示消息
        line_bot_api.reply_message(
            event.reply_token,
            #TextSendMessage(text="你無權使用這個功能。")
            TextSendMessage(text=f"你無權使用這個功能，請聯絡管理員將ID加入白名單。你的 User ID 是: {user_id}")
        )
        return
 
    if event.message.type != "text":
        return

    if event.message.text == "新聞":
        
        reply_msg = scrape_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg)
        )
        return
    
    gemini.add_msg(f"HUMAN:{event.message.text}?\n")
    reply_msg = gemini.get_response().replace("AI:", "", 1)
    gemini.add_msg(f"AI:{reply_msg}\n")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_msg)
    )


if __name__ == "__main__":
    app.run()
