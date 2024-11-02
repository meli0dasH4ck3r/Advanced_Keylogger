import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Bot info and chat id
API_TOKEN = os.getenv('API_TOKEN') 
CHAT_ID  = os.getenv('CHAT_ID')
TELEGRAM_URL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'

# Check new messages from Telegram
def check_telegram(last_update_id):
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates?offset={last_update_id+1}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        messages = response.json().get('result', [])
        if messages:
            last_message = messages[-1].get('message', {})
            return last_message.get("text"), last_message.get("message_id"), messages[-1].get('update_id')
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Telegram API: {str(e)}")
    return None, None, last_update_id

# Send a message to Telegram
def send_telegram(message):
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        print(response.json())
        response.raise_for_status()  # Raise an error for bad responses
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {str(e)}")
        return None

last_update_id = 0 
text, message_id, last_update_id = check_telegram(last_update_id)

check_telegram(last_update_id) 
send_telegram('Hello! My name is mini_meli0das, a mini version of meli0dasH4ck3r. How can I help you?')