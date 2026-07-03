from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записатись")],
            [KeyboardButton(text="Мої заявки")],
        ],
        resize_keyboard=True,
    )


def confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Підтвердити", callback_data="booking_confirm"),
                InlineKeyboardButton(text="❌ Скасувати", callback_data="booking_cancel"),
            ]
        ]
    )
