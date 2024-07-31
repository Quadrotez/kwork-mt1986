import asyncio
import json
from configparser import ConfigParser

from functions import *
from variables import *

while True:
    while True:
        name_sess = input('Введите имя для вашей сессии: ')

        if os.path.exists(session_path.format(name_sess)):
            break

        if name_sess and input('Сессии не существует. Создать новую? (y/n): ') == 'y':
            init.session(name_sess)
            break

    app = init.client(name_sess)

    (config_sending := ConfigParser()).read(config_sending_path.format(name_sess, encoding=encoding))

    if app:
        break


while True:

    func = input(console_default.get())

    if func == 'sending':
        console_default.add('sending')
        asyncio.run(sending.run(name_sess, config_sending, app))

    elif func == 'set_chats':
        console_default.add('set_chats')

        chats_sending = []

        while True:
            chat = input(console_default.get())

            if chat == 'all':
                break

            chats_sending.append(chat)

        config_sending['GENERAL']['CHATS'] = json.dumps(chats_sending)
        config_sending.write(open(config_sending_path.format(name_sess), 'w', encoding=encoding))

        console_default.cprint('Успешно!')
        console_default.remove()



