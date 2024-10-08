import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import requests

# 設置 Flask 應用，並指定靜態文件夾的絕對路徑
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '../frontend/dist'))

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
    """處理靜態文件和 SPA 路徑"""
    try:
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    except FileNotFoundError:
        return "File not found", 404

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """API 用於發送消息到 LINE Notify"""
    account = request.form.get('account')
    message_key = request.form.get('message')

    if not account or not message_key:
        return jsonify({'status': 'error', 'message': 'Missing account or message parameter'}), 400

    # 使用 MESSAGE_MAP 獲取對應的訊息
    message = MESSAGE_MAP.get(message_key, message_key)
    success = send_to_line(account, message)
    
    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to send message'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
