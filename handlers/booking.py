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
@router.message(F.text == "Записатись")
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.set_state(BookingStates.waiting_for_name)
    await message.answer(
        "Оформимо заявку. Введіть ваше ім'я:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Немає активної заявки для скасування.")
        return
    await state.clear()
    await message.answer(
        "❌ Оформлення заявки скасовано.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("my_bookings"))
@router.message(F.text == "Мої заявки")
async def cmd_my_bookings(message: Message) -> None:
    bookings = await get_user_bookings(message.from_user.id)
    if not bookings:
        await message.answer("У вас немає активних заявок.")
        return

    lines = ["📋 Ваші активні заявки:\n"]
    for b in bookings:
        lines.append(
            f"#{b.id} — {b.date} о {b.time}\n"
            f"Ім'я: {b.name}\n"
            f"Опис: {b.description}\n"
            f"Статус: {b.status}\n"
        )
    await message.answer("\n".join(lines))


@router.message(BookingStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть ім'я текстом.")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(BookingStates.waiting_for_date)
    await message.answer("Введіть бажану дату у форматі ДД.ММ (наприклад, 10.07):")


@router.message(BookingStates.waiting_for_date)
async def process_date(message: Message, state: FSMContext) -> None:
    if not message.text or not is_valid_date(message.text):
        await message.answer(
            "Невірний формат дати. Введіть дату у форматі ДД.ММ, наприклад 10.07:"
        )
        return
    await state.update_data(date=message.text.strip())
    await state.set_state(BookingStates.waiting_for_time)
    await message.answer("Введіть бажаний час у форматі ГГ:ХХ (наприклад, 14:30):")


@router.message(BookingStates.waiting_for_time)
async def process_time(message: Message, state: FSMContext) -> None:
    if not message.text or not is_valid_time(message.text):
        await message.answer(
            "Невірний формат часу. Введіть час у форматі ГГ:ХХ, наприклад 14:30:"
        )
        return
    await state.update_data(time=message.text.strip())
    await state.set_state(BookingStates.waiting_for_description)
    await message.answer("Опишіть коротко ваш запит / послугу:")


@router.message(BookingStates.waiting_for_description)
async def process_description(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, опишіть запит текстом.")
        return
    await state.update_data(description=message.text.strip())
    data = await state.get_data()

    summary = (
        "Перевірте заявку:\n\n"
        f"👤 Ім'я: {data['name']}\n"
        f"📅 Дата: {data['date']}\n"
        f"🕐 Час: {data['time']}\n"
        f"📝 Опис: {data['description']}\n\n"
        "Підтвердити запис?"
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
        "✅ Заявку збережено! Ми зв'яжемось з вами найближчим часом."
    )
    await callback.message.answer("Оберіть дію:", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(BookingStates.waiting_for_confirmation, F.data == "booking_cancel")
async def cancel_booking_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Оформлення заявки скасовано.")
    await callback.message.answer("Оберіть дію:", reply_markup=main_menu_keyboard())
    await callback.answer()
