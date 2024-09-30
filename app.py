from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

LINE_NOTIFY_TOKEN = '8AAY6yR18LUFC5wnsBVOsjSRBHjaawFE5nwilD4cFkn'  # 替換為你的 LINE Notify Token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        headers = {
            "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {'message': message}
        response = requests.post(
            "https://notify-api.line.me/api/notify",
            headers=headers,
            data=data
        )
        if response.status_code == 200:
            return redirect(url_for('index'))
    return "Error in sending message", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
