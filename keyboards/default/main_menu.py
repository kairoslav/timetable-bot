from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Какая сейчас пара?")
        ],
        [
            KeyboardButton(text="Расписание на сегодня")
        ],
        [
            KeyboardButton(text="Расписание на определенный день")
        ]
    ],
    resize_keyboard=True
)