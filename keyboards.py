 HEAD
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить заявку")],
    ],
    resize_keyboard=True
)

direction_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Реклама за товар/услугу", callback_data="dir:ad_for_product")],
        [InlineKeyboardButton(text="🎁 Товар/услуга за рекламу", callback_data="dir:product_for_ad")]
    ]
)

category_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍫 Продукт", callback_data="cat:Продукт")],
        [InlineKeyboardButton(text="💼 Услуги", callback_data="cat:Услуги")],
        [InlineKeyboardButton(text="📦 Другое", callback_data="cat:Другое")]
    ]
)

back_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить заявку")],
    ],
    resize_keyboard=True
)

direction_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Реклама за товар/услугу", callback_data="dir:ad_for_product")],
        [InlineKeyboardButton(text="🎁 Товар/услуга за рекламу", callback_data="dir:product_for_ad")]
    ]
)

category_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍫 Продукт", callback_data="cat:Продукт")],
        [InlineKeyboardButton(text="💼 Услуги", callback_data="cat:Услуги")],
        [InlineKeyboardButton(text="📦 Другое", callback_data="cat:Другое")]
    ]
)

back_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)
 276fa27 (Initial commit)
