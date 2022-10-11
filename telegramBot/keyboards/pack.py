from keyboards.base import BaseKeyboard


class PackKeyboardButtons:
    accept = "Запаковать!"


class PackAgainKeyboardButtons:
    again = "Еще один архив"


class PackKeyboard(BaseKeyboard):
    buttons_list = [
        PackKeyboardButtons.accept
    ]


class PackAgainKeyboard(BaseKeyboard):
    buttons_list = [
        PackAgainKeyboardButtons.again
    ]
