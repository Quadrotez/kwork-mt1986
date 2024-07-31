import os

from functions import init
from variables import *

print()

os.makedirs(sessions_path, exist_ok=True)

config = init.config()

db, cursor = init.database()

