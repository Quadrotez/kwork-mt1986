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
from pyrogram import Client, enums
from pyrogram.errors import PasswordHashInvalid
from pyrogram.errors.exceptions.bad_request_400 import PhoneCodeInvalid, PeerIdInvalid, UsernameInvalid
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from pyrogram.errors.exceptions.unauthorized_401 import SessionPasswordNeeded, AuthKeyUnregistered
from pyrogram.types import InputMediaPhoto


async def run(name_sess: str, config_sending: ConfigParser, app: Client):
    console_default.cprint(f'Начало! Чтобы остановить рассылку, нажмите {stop_key}')

    running = True

    def stop():
        nonlocal running
        keyboard.remove_hotkey(stop_key)
        console_default.cprint('Конец')
        console_default.remove()
        running = False
        return

    keyboard.add_hotkey(stop_key, stop)

    async with app:
        while running:
            chats = json.loads(config_sending['GENERAL']['CHATS'])
            text = config_sending['GENERAL']['TEXT'].replace(r'\n', '\n')
            delay = int(config_sending['GENERAL']['DELAY'])

            for chat in chats:
                old_chat = chat
                try:
                    if '\\' in chat or '/' in chat:
                        chat = chat.split('/')[-1]

                    chat = (await app.get_chat(chat)).id
                    if config_sending['GENERAL'].get('PHOTO'):
                        photo_paths = config_sending['GENERAL']['PHOTO'].split(' ')

                        c = False
                        result_photos = []
                        for i in photo_paths:
                            if not c:
                                c = True
                                result_photos.append(InputMediaPhoto(BytesIO(open(i, 'rb').read()), caption=text,
                                                                     parse_mode=enums.ParseMode.MARKDOWN))
                            else:
                                result_photos.append(InputMediaPhoto(BytesIO(open(i, 'rb').read())))
                        await app.send_media_group(chat,
                                                   media=result_photos)

                    else:
                        await app.send_message(chat, text, parse_mode=enums.ParseMode.MARKDOWN)

                except (PeerIdInvalid, UsernameInvalid):
                    print(f'Чат не обнаружен: {old_chat} ({chat})')
                    pass

            end_time = time.time() + delay

            while time.time() < end_time:
                if not running:
                    return

                await asyncio.sleep(0.1)
