from fastapi import FastAPI , HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.gemini import Gemini

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
        "U12c2b60e458a682b63ad793e325613df"
    ]  # 允許的 user_id 清單
    #U34651e48067cdde9fb6df533b53e367c 隆
    #U092b3fc3dcef603a0fc0a56000468e1d 不路
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
    
    gemini.add_msg(f"HUMAN:{event.message.text}?\n")
    reply_msg = gemini.get_response().replace("AI:", "", 1)
    gemini.add_msg(f"AI:{reply_msg}\n")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_msg)
    )


if __name__ == "__main__":
    app.run()
