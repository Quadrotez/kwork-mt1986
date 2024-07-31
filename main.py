import os

from functions import *
from variables import *
from pyrogram import Client, types

while True:
    name_sess = input('Введите имя для вашей сессии: ')

    if not os.path.exists(session_path.format(name_sess)):
        init.session(name_sess)

    else:
        app = init.client(name_sess)

        if app:
            break


while True:
    func = input('./ ')
