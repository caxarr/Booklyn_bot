from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID
from database import get_all_bookings
from utils import chunk_text

router = Router()


@router.message(Command("all_bookings"))
async def cmd_all_bookings(message: Message) -> None:
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ This command is only available to the administrator.")
        return

    bookings = await get_all_bookings()
    if not bookings:
        await message.answer("There are no bookings yet.")
        return

    lines = [f"Total bookings: {len(bookings)}\n"]
    for b in bookings:
        username = f"@{b.username}" if b.username else "—"
        lines.append(
            f"#{b.id} | {b.status}\n"
            f"Name: {b.name} | User: {username} (id {b.user_id})\n"
            f"Date/time: {b.date} {b.time}\n"
            f"Description: {b.description}\n"
            f"Created: {b.created_at}\n"
        )

    for chunk in chunk_text("\n".join(lines)):
        await message.answer(chunk)
