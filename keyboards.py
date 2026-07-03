from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Book now")],
            [KeyboardButton(text="My bookings")],
        ],
        resize_keyboard=True,
    )


def confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Confirm", callback_data="booking_confirm"),
                InlineKeyboardButton(text="❌ Cancel", callback_data="booking_cancel"),
            ]
        ]
    )
