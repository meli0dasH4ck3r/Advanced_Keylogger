import pytest
from dotenv import load_dotenv
import requests
import os
import requests_mock
from telegram import check_telegram, send_telegram

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN') 
CHAT_ID  = os.getenv('CHAT_ID')
TELEGRAM_URL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'


# Test case 1: Multiple messages, checking for the last message in the response
def test_check_telegram_multiple_messages(requests_mock):
    last_update_id = 123
    requests_mock.get(f'https://api.telegram.org/bot{API_TOKEN}/getUpdates?offset={last_update_id+1}', json={
        "ok": True,
        "result": [
            {"update_id": 124, "message": {"message_id": 1, "text": "First message"}},
            {"update_id": 125, "message": {"message_id": 2, "text": "Second message"}},
            {"update_id": 126, "message": {"message_id": 3, "text": "Final message"}}
        ]
    })
    text, message_id, update_id = check_telegram(last_update_id)
    assert text == "Final message"
    assert message_id == 3
    assert update_id == 126


# Test case 2: Invalid response from API without 'result' field
def test_check_telegram_invalid_response(requests_mock):
    last_update_id = 123
    requests_mock.get(f'https://api.telegram.org/bot{API_TOKEN}/getUpdates?offset={last_update_id+1}', json={
        "ok": True  # Missing 'result'
    })
    text, message_id, update_id = check_telegram(last_update_id)
    assert text is None
    assert message_id is None
    assert update_id == 123

# Test case 3: HTTP error response from API
def test_check_telegram_http_error(requests_mock):
    last_update_id = 123
    requests_mock.get(f'https://api.telegram.org/bot{API_TOKEN}/getUpdates?offset={last_update_id+1}', status_code=500)
    
    text, message_id, update_id = check_telegram(last_update_id)
    assert text is None
    assert message_id is None
    assert update_id == 123

# Test case 4: Duplicate update IDs in API response
def test_check_telegram_duplicate_update_id(requests_mock):
    last_update_id = 123
    requests_mock.get(f'https://api.telegram.org/bot{API_TOKEN}/getUpdates?offset={last_update_id+1}', json={
        "ok": True,
        "result": [
            {"update_id": 124, "message": {"message_id": 1, "text": "Message 1"}},
            {"update_id": 124, "message": {"message_id": 2, "text": "Duplicate message"}}
        ]
    })
    text, message_id, update_id = check_telegram(last_update_id)
    assert text == "Duplicate message"
    assert message_id == 2
    assert update_id == 124  # Update ID should reflect the latest entry
