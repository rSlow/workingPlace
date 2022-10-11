from .base import BaseKeyboard


class StartKeyboard(BaseKeyboard):
    class Buttons:
        pack = "Запаковать 💼"

    buttons_list = [
        Buttons.pack
    ]
