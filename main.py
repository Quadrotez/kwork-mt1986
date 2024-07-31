import os

from functions import *
from variables import *
from pyrogram import Client, types

while True:
    while True:
        name_sess = input('Введите имя для вашей сессии: ')

        if not os.path.exists(session_path.format(name_sess)):
            init.session(name_sess)

        else:
            break

    app = init.client(name_sess)

    if app:
        break


app.connect()
app.send_message('me', 'Hi')
app.send_dice()

print('Ok')
