from .base import BaseKeyboard


class StartKeyboard(BaseKeyboard):
    class Buttons:
        pack = "Запаковать 💼"
        download_video_note = "Скачать кружочек 📹"
        convert_voice = "Конвертировать голосовое 🎤"

    add_on_main_button = False
    buttons_list = [
        Buttons.pack,
        Buttons.download_video_note,
        Buttons.convert_voice
    ]
