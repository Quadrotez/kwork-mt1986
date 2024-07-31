import asyncio
import time
import json
from configparser import ConfigParser

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

    keyboard.on_press(stop)

    await app.connect()

    while running:
        chats = json.loads(config_sending['GENERAL']['CHATS'])
        text = config_sending['GENERAL']['TEXT']
        delay = int(config_sending['GENERAL']['DELAY'])

        for chat in chats:
            try:
                await app.send_message(chat, text)
            except PeerIdInvalid:
                print(f'Чат не обнаружен: {chat}')
                pass

        end_time = time.time() + delay

        while time.time() < end_time:
            if not running:
                return

            await asyncio.sleep(0.1)


