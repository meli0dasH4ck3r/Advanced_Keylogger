import pytest
from unittest.mock import patch
from my_module import check_telegram, send_telegram  # Remplacez my_module par le nom réel de votre fichier Python

API_TOKEN = "test_api_token"
CHAT_ID = "test_chat_id"
TELEGRAM_URL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'


# Test simplifié pour la fonction check_telegram
def test_check_telegram(mock_get):
    mock_get.return_value.json.return_value = {
        'result': [
            {'update_id': 123, 'message': {'message_id': 1, 'text': 'Test message'}}
        ]
    }
    mock_get.return_value.status_code = 200

    text, message_id, update_id = check_telegram(last_update_id=122)
    
    assert text == "Test message"
    assert message_id == 1
    assert update_id == 123


# Test simplifié pour la fonction send_telegram
def test_send_telegram(mock_post):
    mock_post.return_value.status_code = 200

    status_code = send_telegram("Hello, this is a test message.")
    
    assert status_code == 200
    mock_post.assert_called_once_with(
        TELEGRAM_URL,
        data={'chat_id': CHAT_ID, 'text': "Hello, this is a test message."}
    )
