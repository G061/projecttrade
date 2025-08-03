"""
Telegram and Pushbullet alert utility
"""
import os
import requests

def send_telegram_alert(message):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        print("Telegram credentials not set.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def send_pushbullet_alert(message):
    api_key = os.getenv('PUSHBULLET_API_KEY')
    if not api_key:
        print("Pushbullet API key not set.")
        return
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {"Access-Token": api_key, "Content-Type": "application/json"}
    data = {"type": "note", "body": message}
    requests.post(url, headers=headers, json=data)
