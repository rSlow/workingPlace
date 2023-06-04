from keyboards.base import BaseKeyboard


class ConvertVideoKeyboard(BaseKeyboard):
    pass


class ConvertAgainVideoKeyboard(BaseKeyboard):
    class Buttons:
        again = "Еще одно 🔄"

    buttons_list = [
        Buttons.again
    ]
