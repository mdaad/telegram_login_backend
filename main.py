from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Token Backend Running!"

@app.route("/send_token", methods=["POST"])
def send_token():
    data = request.get_json()
    telegram_id = data.get("telegram_id")

    if not telegram_id:
        return jsonify({"error": "Missing telegram_id"}), 400

    token = str(random.randint(100000, 999999))
    print(f"Sending token {token} to Telegram ID: {telegram_id}")

    # Yahan Telegram bot se message bhejne ka logic aayega
    # Jaise: bot.send_message(chat_id=telegram_id, text=f"Your login token: {token}")

    return jsonify({"message": "Token sent successfully", "token": token})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
