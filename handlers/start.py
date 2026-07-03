from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards import main_menu_keyboard

router = Router()

WELCOME_TEXT = (
    "👋 Welcome!\n\n"
    "I'm a bot for booking a consultation / service.\n\n"
    "Here's what I can do:\n"
    "• /book or the \"Book now\" button — create a new booking\n"
    "• /my_bookings — view your active bookings\n"
    "• /cancel — cancel a booking that's currently being filled in\n\n"
    "To get started, tap \"Book now\" or send /book."
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())
