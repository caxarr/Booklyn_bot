from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards import main_menu_keyboard

router = Router()

WELCOME_TEXT = (
    "👋 Вітаю!\n\n"
    "Я бот для запису на консультацію / бронювання послуги.\n\n"
    "Що я вмію:\n"
    "• /book або кнопка «Записатись» — оформити нову заявку\n"
    "• /my_bookings — переглянути ваші активні заявки\n"
    "• /cancel — скасувати оформлення заявки, що в процесі\n\n"
    "Щоб почати, натисніть «Записатись» або надішліть /book."
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())
