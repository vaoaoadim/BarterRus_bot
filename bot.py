 HEAD
import asyncio
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, CHANNEL_ID
from keyboards import main_kb, direction_kb, category_kb, back_button
from database import add_ad, get_last_ad_time
from barter_logic import format_ad

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

user_state = {}

@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer(
        "Привет! Это бот для рекламы по бартеру.\n"
        "Здесь ты можешь оставить свою заявку на обмен рекламой на товар/услугу или наоборот.",
        reply_markup=main_kb
    )

@dp.message()
async def handle_text(msg: Message):
    user_id = msg.from_user.id
    text = msg.text.strip()

    if text == "➕ Добавить заявку":
        last_time = get_last_ad_time(user_id)
        now = int(time.time())

        if last_time and now - last_time < 43200:
            remaining = int((43200 - (now - last_time)) / 60)
            await msg.answer(f"⏳ Ты уже оставлял заявку. Попробуй снова через {remaining} минут.")
            return

        user_state[user_id] = {}
        await msg.answer("Выбери направление обмена:", reply_markup=direction_kb)

    elif text == "🔙 Назад":
        state = user_state.get(user_id, {})
        if "contact" in state:
            del state["contact"]
            await msg.answer("Укажи свой контакт (ник, телеграм или ссылка):", reply_markup=back_button)
        elif "description" in state:
            del state["description"]
            await msg.answer("Теперь опиши подробнее, что ты предлагаешь или ищешь:", reply_markup=back_button)
        elif "title" in state:
            del state["title"]
            await msg.answer("Введи краткий заголовок своей заявки:", reply_markup=back_button)
        elif "category" in state:
            del state["category"]
            await msg.answer("Выбери категорию:", reply_markup=category_kb)
        elif "direction" in state:
            del state["direction"]
            await msg.answer("Выбери направление обмена:", reply_markup=direction_kb)
        else:
            user_state.pop(user_id, None)
            await msg.answer("Вы вернулись в главное меню.", reply_markup=main_kb)

    elif user_id in user_state:
        state = user_state[user_id]
        if "title" not in state:
            state["title"] = text
            await msg.answer("Теперь опиши подробнее, что ты предлагаешь или ищешь:", reply_markup=back_button)
        elif "description" not in state:
            state["description"] = text
            await msg.answer("Укажи свой контакт (ник, телеграм или ссылка):", reply_markup=back_button)
        elif "contact" not in state:
            state["contact"] = text
            add_ad(
                user_id=user_id,
                direction=state["direction"],
                category=state["category"],
                title=state["title"],
                description=state["description"],
                contact=state["contact"]
            )
            # Отправка в канал
            await bot.send_message(CHANNEL_ID, format_ad((
                None, state["direction"], state["category"],
                state["title"], state["description"], state["contact"]
            )))
            await msg.answer("✅ Твоя заявка сохранена и отправлена в каталог!\nВозвращайся через 12 часов, чтобы создать новую.", reply_markup=main_kb)
            del user_state[user_id]

@dp.callback_query(F.data.startswith("dir:"))
async def choose_category(callback: CallbackQuery):
    direction = callback.data.split(":")[1]
    user_state[callback.from_user.id] = {"direction": direction}
    await callback.message.answer("Выбери категорию:", reply_markup=category_kb)

@dp.callback_query(F.data.startswith("cat:"))
async def ask_title(callback: CallbackQuery):
    category = callback.data.split(":")[1]
    user_state[callback.from_user.id]["category"] = category
    await callback.message.answer("Введи краткий заголовок своей заявки:", reply_markup=back_button)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, CHANNEL_ID
from keyboards import main_kb, direction_kb, category_kb, back_button
from database import add_ad, get_last_ad_time
from barter_logic import format_ad

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

user_state = {}

@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer(
        "Привет! Это бот для рекламы по бартеру.\n"
        "Здесь ты можешь оставить свою заявку на обмен рекламой на товар/услугу или наоборот.",
        reply_markup=main_kb
    )

@dp.message()
async def handle_text(msg: Message):
    user_id = msg.from_user.id
    text = msg.text.strip()

    if text == "➕ Добавить заявку":
        last_time = get_last_ad_time(user_id)
        now = int(time.time())

        if last_time and now - last_time < 43200:
            remaining = int((43200 - (now - last_time)) / 60)
            await msg.answer(f"⏳ Ты уже оставлял заявку. Попробуй снова через {remaining} минут.")
            return

        user_state[user_id] = {}
        await msg.answer("Выбери направление обмена:", reply_markup=direction_kb)

    elif text == "🔙 Назад":
        state = user_state.get(user_id, {})
        if "contact" in state:
            del state["contact"]
            await msg.answer("Укажи свой контакт (ник, телеграм или ссылка):", reply_markup=back_button)
        elif "description" in state:
            del state["description"]
            await msg.answer("Теперь опиши подробнее, что ты предлагаешь или ищешь:", reply_markup=back_button)
        elif "title" in state:
            del state["title"]
            await msg.answer("Введи краткий заголовок своей заявки:", reply_markup=back_button)
        elif "category" in state:
            del state["category"]
            await msg.answer("Выбери категорию:", reply_markup=category_kb)
        elif "direction" in state:
            del state["direction"]
            await msg.answer("Выбери направление обмена:", reply_markup=direction_kb)
        else:
            user_state.pop(user_id, None)
            await msg.answer("Вы вернулись в главное меню.", reply_markup=main_kb)

    elif user_id in user_state:
        state = user_state[user_id]
        if "title" not in state:
            state["title"] = text
            await msg.answer("Теперь опиши подробнее, что ты предлагаешь или ищешь:", reply_markup=back_button)
        elif "description" not in state:
            state["description"] = text
            await msg.answer("Укажи свой контакт (ник, телеграм или ссылка):", reply_markup=back_button)
        elif "contact" not in state:
            state["contact"] = text
            add_ad(
                user_id=user_id,
                direction=state["direction"],
                category=state["category"],
                title=state["title"],
                description=state["description"],
                contact=state["contact"]
            )
            # Отправка в канал
            await bot.send_message(CHANNEL_ID, format_ad((
                None, state["direction"], state["category"],
                state["title"], state["description"], state["contact"]
            )))
            await msg.answer("✅ Твоя заявка сохранена и отправлена в каталог!\nВозвращайся через 12 часов, чтобы создать новую.", reply_markup=main_kb)
            del user_state[user_id]

@dp.callback_query(F.data.startswith("dir:"))
async def choose_category(callback: CallbackQuery):
    direction = callback.data.split(":")[1]
    user_state[callback.from_user.id] = {"direction": direction}
    await callback.message.answer("Выбери категорию:", reply_markup=category_kb)

@dp.callback_query(F.data.startswith("cat:"))
async def ask_title(callback: CallbackQuery):
    category = callback.data.split(":")[1]
    user_state[callback.from_user.id]["category"] = category
    await callback.message.answer("Введи краткий заголовок своей заявки:", reply_markup=back_button)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
 276fa27 (Initial commit)
