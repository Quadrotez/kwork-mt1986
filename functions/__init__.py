import os

from functions import init, sending, console_default
from variables import *

print()

os.makedirs(sessions_path, exist_ok=True)

config = init.config()

db, cursor = init.database()

