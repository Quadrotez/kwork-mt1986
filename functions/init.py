import json
import os
from pathlib import Path
import sqlite3
from configparser import ConfigParser
from variables import *
from pyrogram import Client
from pyrogram.errors import PasswordHashInvalid
from pyrogram.errors.exceptions.bad_request_400 import PhoneCodeInvalid
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from pyrogram.errors.exceptions.unauthorized_401 import SessionPasswordNeeded, AuthKeyUnregistered


def config():
    if not os.path.exists(config_path):
        open(config_path, 'w', encoding=encoding).write('')
        (l_config := ConfigParser()).read(config_path, encoding=encoding)
        l_config.add_section('GENERAL')
        print(f'''Приложению потребуются некоторые ваши данные. 
Введите их. Это потребуется сделать только один раз, 
после чего вы всегда сможете изменить значения в файле {config_path}''')
        l_config['GENERAL']['API_ID'] = input('API-ID: ')
        l_config['GENERAL']['API_HASH'] = input('API-HASH: ')
        l_config.write(open(config_path, 'w', encoding=encoding))

        print('Спасибо!')


def session(name_sess):
    (l_config := ConfigParser()).read(config_path, encoding=encoding)

    os.makedirs(f'{sessions_path}/{name_sess}', exist_ok=True)

    app = client(name_sess, just_app=True)
    app.connect()

    while True:
        phone_number = input("Введите ваш номер телефона: ")
        try:
            sent_code_info = app.send_code(phone_number)
            break
        except PhoneNumberInvalid:
            print('Номер телефона неверный! Попробуйте ещё раз!')

    phone_code = input("Код был выслан. Введите его, пожалуйста: ")
    while True:
        try:
            app.sign_in(phone_number, sent_code_info.phone_code_hash, phone_code)
            break

        except PhoneCodeInvalid:
            print('Код неправильный!')
            phone_code = input("Введите код: ")

        except SessionPasswordNeeded:
            password = input("У вас стоит пароль. Введите его: ")
            while True:
                try:
                    app.check_password(password)
                    break
                except PasswordHashInvalid:
                    print('Пароль неверный!')
                    password = input("Введите пароль: ")

    app.disconnect()

    open(config_sending_path.format(name_sess), 'w', encoding=encoding).write('')

    (config_sending := ConfigParser()).read(config_sending_path, encoding=encoding)

    config_sending.add_section('GENERAL')
    config_sending['GENERAL']['TEXT'] = 'TEXT'
    config_sending['GENERAL']['CHATS'] = json.dumps([])
    config_sending['GENERAL']['DELAY'] = '20'
    config_sending.write(open(config_sending_path.format(name_sess), 'w', encoding=encoding))


def database():
    db = sqlite3.connect(database_path)

    cursor = db.cursor()

    return db, cursor


def proxy_dict():
    (l_config := ConfigParser()).read(config_path, encoding=encoding)
    if l_config.has_section('PROXY'):
        return {
            "connection_type": l_config['PROXY']['CONNECTION_TYPE'],
            "hostname": l_config['PROXY']['HOST'],
            "port": l_config['PROXY']['PORT'],
            "username": l_config['PROXY']['LOGIN'],
            "password": l_config['PASSWORD']}
    else:
        return


def client(name_sess: str, just_app: bool = False):
    (l_config := ConfigParser()).read(config_path, encoding=encoding)
    app = Client(name=session_path.format(name_sess).rpartition('.')[0], api_id=l_config['GENERAL']['API_ID'],
                 api_hash=l_config['GENERAL']['API_HASH'], device_model=device_model, proxy=proxy_dict())

    if just_app:
        return app

    try:
        app.connect(), app.get_me(), app.disconnect()
        return app

    except AuthKeyUnregistered:
        print('Сессия не валидна!')
        app.disconnect() if not app.is_connected else None
        Path('{0}.{1}'.format(session_path.format(name_sess).rpartition('.')[0],
                              'session-journal')).unlink(missing_ok=True)
        os.remove(session_path.format(name_sess))

        return
