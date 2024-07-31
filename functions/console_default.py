console_default = './'


def add(arg):
    global console_default
    console_default = f'{console_default}{arg}/'


def remove():
    global console_default
    console_default = f"{console_default.rpartition('/')[0].rpartition('/')[0]}/"


def get():
    return f'{console_default} '


def cinput():
    return input(get())


def cprint(text: str):
    print(f'{get()}{text}')