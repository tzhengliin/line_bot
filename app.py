from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

# LINE Notify Token 對應不同帳號
LINE_TOKENS = {
    '測試': '8AAY6yR18LUFC5wnsBVOsjSRBHjaawFE5nwilD4cFkn',  
    '王悅': 'APgIjzItUSEk9aelLIQzSxr6ZQKSsGe6xt7cWpEO1US',  
    '佳玫': 'eKhtGiQtthGBZPUys6S4qo5j4RxLa43HUVwUk7zcnsI'  
}

# 代號與完整訊息對應表
MESSAGE_MAP = {
    'later': '等等要吃餐囉!  要吃餐囉!',
    'timeon': '時間到了! 時間到了! 吃餐囉~ 小安好興奮阿',
    'photo1': '照片~照片~我要美食的照片',
    'photo2': '敲碗~照片有拍了嗎?',
    'goodeat': '哇~ 看起來好好吃的感覺',
    'crazy': 'OH~No!!! 照片快來~照片快來~',
    'happy': '歐耶 有照片了~',
    'excellent': '你怎麼這麼優秀!!'
}

def send_to_line(account, message):
    """發送消息到 LINE Notify"""
    token = LINE_TOKENS.get(account)
    if not token:
        return False  # 如果找不到對應的 Token，返回失敗

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {'message': message}
    response = requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        data=data
    )
    return response.status_code == 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>')
def render_page(page):
    try:
        return render_template(f'{page}.html')
    except Exception as e:
        return "Page not found", 404


@app.route('/send_message', methods=['POST'])
def send_message():
    account = request.form.get('account')
    message_key = request.form.get('message')

    if account and message_key:
        # 檢查 MESSAGE_MAP 中是否有對應的代號
        message = MESSAGE_MAP.get(message_key)

        # 如果找不到代號，就認為是自訂訊息
        if not message:
            message = message_key

        # 發送消息
        success = send_to_line(account, message)
        if success:
            return redirect(url_for('index'))
    return "Error in sending message", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
