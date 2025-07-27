import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from config import BOT_TOKEN, GROUP_CHAT_ID
from keyboards import main_kb, direction_kb, category_kb
from database import add_ad
from barter_logic import search_ads, format_ad

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

class AdState(StatesGroup):
    choosing_direction = State()
    choosing_category = State()
    entering_title = State()
    entering_description = State()

user_data = {}

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Что вы хотите сделать?", reply_markup=main_kb)

@dp.message(F.text == "➕ Разместить заявку")
async def create_ad_start(message: Message, state: FSMContext):
    await state.set_state(AdState.choosing_direction)
    await message.answer("Выберите направление обмена:", reply_markup=direction_kb)

@dp.callback_query(AdState.choosing_direction)
async def choose_direction(callback: CallbackQuery, state: FSMContext):
    await state.update_data(direction=callback.data)
    await state.set_state(AdState.choosing_category)
    await callback.message.edit_text("Выберите категорию:", reply_markup=category_kb)

@dp.callback_query(AdState.choosing_category)
async def choose_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await state.set_state(AdState.entering_title)
    await callback.message.edit_text("Введите заголовок вашей заявки:")

@dp.message(AdState.entering_title)
async def enter_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AdState.entering_description)
    await message.answer("Введите описание заявки. Вы также можете прикрепить одно изображение к этому сообщению (не обязательно):")

@dp.message(AdState.entering_description, F.photo)
async def enter_description_with_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    description = message.caption or "(без описания)"
    photo_id = message.photo[-1].file_id
    contact = f"@{message.from_user.username}" if message.from_user.username else f"tg://user?id={message.from_user.id}"

    add_ad(
        data["direction"],
        data["category"],
        data["title"],
        description,
        contact
    )

    text = format_ad((None, data["direction"], data["category"], data["title"], description, contact))

    await message.answer("Ваша заявка опубликована!")
    await bot.send_photo(chat_id=GROUP_CHAT_ID, photo=photo_id, caption=text)

@dp.message(AdState.entering_description)
async def enter_description(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    description = message.text
    contact = f"@{message.from_user.username}" if message.from_user.username else f"tg://user?id={message.from_user.id}"

    add_ad(
        data["direction"],
        data["category"],
        data["title"],
        description,
        contact
    )

    text = format_ad((None, data["direction"], data["category"], data["title"], description, contact))

    await message.answer("Ваша заявка опубликована!")
    await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)

@dp.message(F.text == "🔍 Смотреть заявки")
async def view_ads(message: Message):
    await message.answer("Открыть каталог заявок:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📂 Перейти в канал", url=f"https://t.me/c/{str(GROUP_CHAT_ID).lstrip('-100')}")]
    ]))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
