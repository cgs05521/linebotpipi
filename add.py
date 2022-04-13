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

line_bot_api = LineBotApi('0Osfc8b4cHQ0gZoJ8+SIcTZ7PRgLGE88D4CLBj6TxhRBCNaM++pd1MkylN993HW2ZrGNN76KWsto3wadx3dRd3k020DvRvrX643GcBtFPDWCY12FNBfvH9FZwtTLTnXvKCtfR4dypLG2/p8Bu1WRCgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5d790a182167b0dc68fd58763c033a67')


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