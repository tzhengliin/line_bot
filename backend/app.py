import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import requests

app = Flask(__name__, static_folder='../frontend/dist')

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
@app.route('/<path:path>')
def index(path=''):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/send_message', methods=['POST'])
def send_message():
    account = request.form.get('account')
    message_key = request.form.get('message')

    if account and message_key:
        message = LINE_TOKENS.get(message_key, message_key)
        success = send_to_line(account, message)
        if success:
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Error in sending message'}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)