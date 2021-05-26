from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

chose_day_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пн", callback_data="Пн"), InlineKeyboardButton(text="Вт", callback_data="Вт")
        ],
        [
            InlineKeyboardButton(text="Чт", callback_data="Чт"), InlineKeyboardButton(text="Пт", callback_data="Пт")
        ],
        [
            InlineKeyboardButton(text="Сб", callback_data="Сб"), InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ],
    ]
)