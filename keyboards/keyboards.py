from aiogram.types import KeyboardButton, ReplyKeyboardMarkup  # Обычные кнопки
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  # Инлайн кнопки
from aiogram.enums.dice_emoji import DiceEmoji

# Создаем объекты кнопок
contact_btn = KeyboardButton(
    text='Поділитися номером ☎️👈',
    request_contact=True
)
# Меню старт
keyboard_start = ReplyKeyboardMarkup(keyboard=[[contact_btn]],
                                     one_time_keyboard=True,  # Сварачивать клавиатуру
                                     resize_keyboard=True)  # Растянуть кнопки

# Создаем объекты инлайн-кнопок
button_stock = InlineKeyboardButton(
    text='Акції 💰',
    callback_data='button_stock_clik'
)

button_dice = InlineKeyboardButton(
    text='Кубик 🎲',
    callback_data='button_dice_clik'
)

button_basketball = InlineKeyboardButton(
    text='Баскет 🏀',
    callback_data='button_basketball_clik'
)

# Создаем объект инлайн-клавиатуры
keyboard_inline = InlineKeyboardMarkup(
    inline_keyboard=[[button_stock],
                     [button_dice],
                     [button_basketball]],
    resize_keyboard=True
)
