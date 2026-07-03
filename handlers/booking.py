from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from database import add_booking, get_user_bookings
from keyboards import confirmation_keyboard, main_menu_keyboard
from states import BookingStates
from utils import is_valid_date, is_valid_time

router = Router()


@router.message(Command("book"))
@router.message(F.text == "Book now")
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.set_state(BookingStates.waiting_for_name)
    await message.answer(
        "Let's create a booking. Please enter your name:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("There is no active booking to cancel.")
        return
    await state.clear()
    await message.answer(
        "❌ Booking process cancelled.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("my_bookings"))
@router.message(F.text == "My bookings")
async def cmd_my_bookings(message: Message) -> None:
    bookings = await get_user_bookings(message.from_user.id)
    if not bookings:
        await message.answer("You don't have any active bookings.")
        return

    lines = ["📋 Your active bookings:\n"]
    for b in bookings:
        lines.append(
            f"#{b.id} — {b.date} at {b.time}\n"
            f"Name: {b.name}\n"
            f"Description: {b.description}\n"
            f"Status: {b.status}\n"
        )
    await message.answer("\n".join(lines))


@router.message(BookingStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.strip():
        await message.answer("Please enter your name as text.")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(BookingStates.waiting_for_date)
    await message.answer("Enter the desired date in DD.MM format (e.g. 10.07):")


@router.message(BookingStates.waiting_for_date)
async def process_date(message: Message, state: FSMContext) -> None:
    if not message.text or not is_valid_date(message.text):
        await message.answer(
            "Invalid date format. Please enter the date as DD.MM, e.g. 10.07:"
        )
        return
    await state.update_data(date=message.text.strip())
    await state.set_state(BookingStates.waiting_for_time)
    await message.answer("Enter the desired time in HH:MM format (e.g. 14:30):")


@router.message(BookingStates.waiting_for_time)
async def process_time(message: Message, state: FSMContext) -> None:
    if not message.text or not is_valid_time(message.text):
        await message.answer(
            "Invalid time format. Please enter the time as HH:MM, e.g. 14:30:"
        )
        return
    await state.update_data(time=message.text.strip())
    await state.set_state(BookingStates.waiting_for_description)
    await message.answer("Briefly describe your request / the service you need:")


@router.message(BookingStates.waiting_for_description)
async def process_description(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.strip():
        await message.answer("Please describe your request as text.")
        return
    await state.update_data(description=message.text.strip())
    data = await state.get_data()

    summary = (
        "Please review your booking:\n\n"
        f"👤 Name: {data['name']}\n"
        f"📅 Date: {data['date']}\n"
        f"🕐 Time: {data['time']}\n"
        f"📝 Description: {data['description']}\n\n"
        "Confirm the booking?"
    )
    await state.set_state(BookingStates.waiting_for_confirmation)
    await message.answer(summary, reply_markup=confirmation_keyboard())


@router.callback_query(BookingStates.waiting_for_confirmation, F.data == "booking_confirm")
async def confirm_booking(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await add_booking(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        name=data["name"],
        date=data["date"],
        time=data["time"],
        description=data["description"],
    )
    await state.clear()
    await callback.message.edit_text(
        "✅ Booking saved! We'll get in touch with you soon."
    )
    await callback.message.answer("Choose an action:", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(BookingStates.waiting_for_confirmation, F.data == "booking_cancel")
async def cancel_booking_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Booking process cancelled.")
    await callback.message.answer("Choose an action:", reply_markup=main_menu_keyboard())
    await callback.answer()
