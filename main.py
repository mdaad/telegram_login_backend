from flask import Flask, request, jsonify
import random, json, time
from telegram import Bot

app = Flask(__name__)
bot_token = "7848313142:AAG3EbL9OLkM4xvMFOCDZ19Aix3CPhgh0bQ"
bot = Bot(token=bot_token)

@app.route('/send-token', methods=['POST'])
def send_token():
    data = request.get_json()
    username = data['username']
    token = str(random.randint(100000, 999999))

    try:
        bot.send_message(chat_id=f"@{username}", text=f"Your login token: {token}")

        with open('tokens.json', 'r+') as file:
            try:
                tokens = json.load(file)
            except:
                tokens = {}

            tokens[username] = {
                "token": token,
                "expiry": time.time() + 300
            }

            file.seek(0)
            json.dump(tokens, file)
            file.truncate()

        return jsonify({"success": True, "message": "Token sent!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.get_json()
    username = data['username']
    token = data['token']

    with open('tokens.json', 'r') as file:
        tokens = json.load(file)

    if username in tokens:
        saved = tokens[username]
        if saved['token'] == token and time.time() < saved['expiry']:
            return jsonify({"success": True, "message": "Verified!"})

    return jsonify({"success": False, "message": "Invalid or expired token."})

@app.route('/')
def home():
    return "Bot is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
