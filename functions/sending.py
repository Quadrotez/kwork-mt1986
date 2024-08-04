import asyncio
import os.path
import sys
import time
import json
from configparser import ConfigParser
from io import BytesIO
import keyboard

from functions import console_default
from variables import *
from pyrogram import Client
from pyrogram.errors import PasswordHashInvalid
from pyrogram.errors.exceptions.bad_request_400 import PhoneCodeInvalid, PeerIdInvalid
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from pyrogram.errors.exceptions.unauthorized_401 import SessionPasswordNeeded, AuthKeyUnregistered


async def run(name_sess: str, config_sending: ConfigParser, app: Client):
    console_default.cprint(f'Начало! Чтобы остановить рассылку, нажмите {stop_key}')

    running = True

    def stop(event: keyboard.KeyboardEvent):
        nonlocal running
        if event.name == stop_key:
            console_default.cprint('Конец')
            console_default.remove()
            running = False
            return

    keyboard.on_press(stop)

    async with app:

        while running:
            chats = json.loads(config_sending['GENERAL']['CHATS'])
            text = config_sending['GENERAL']['TEXT'].replace(r'\n', '\n')
            delay = int(config_sending['GENERAL']['DELAY'])

            for chat in chats:
                try:
                    if config_sending['GENERAL'].get('PHOTO'):
                        photo_path = config_sending['GENERAL']['PHOTO']
                        if not os.path.exists(photo_path):
                            print(f'Путь к фото некорректный! {photo_path}')

                        else:
                            await app.send_photo(chat,
                                                 photo=BytesIO(open(photo_path, 'rb').read()),
                                                 caption=text)


                    else:
                        await app.send_message(chat, text)

                except PeerIdInvalid:
                    print(f'Чат не обнаружен: {chat}')
                    pass

            end_time = time.time() + delay

            while time.time() < end_time:
                if not running:
                    return

                await asyncio.sleep(0.1)
