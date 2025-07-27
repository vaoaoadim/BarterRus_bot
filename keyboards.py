from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Разместить заявку")],
        [KeyboardButton(text="🔍 Смотреть заявки")]
    ],
    resize_keyboard=True
)

direction_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 Реклама за товар/услугу", callback_data="ad_for_product")],
    [InlineKeyboardButton(text="🎁 Товар/услуга за рекламу", callback_data="product_for_ad")]
])

category_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💼 Услуги", callback_data="Услуги")],
    [InlineKeyboardButton(text="🛍 Товары", callback_data="Товары")],
    [InlineKeyboardButton(text="📢 Реклама", callback_data="Реклама")],
    [InlineKeyboardButton(text="📦 Другое", callback_data="Другое")]
])
