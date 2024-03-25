from aiogram import Bot
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

# заблокирован бот
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated

# Отправка файла
from aiogram.types import FSInputFile

# Фильтр: проверка админа
from filters.filters import IsAdmin

# Клавиатура
from keyboards.keyboards import keyboard_start, keyboard_inline

# Работа с БД
from config_data.config_db_sqlite import (select_users, add_users, update_users,
                                          select_active_users)

# Настройки конфигурации
from config_data.config import Config, load_config

# Вытягиваем путь к БД
config: Config = load_config()
path_sqlite = config.path_sqlite.path_sqlite

# Путь к изображению акции
path_img_sale = config.path_img_sale

# Список с ID администраторов бота.
admin_ids_list: list[int] = config.tg_bot.admin_ids

router = Router()


# Собственный фильтр, проверяющий юзера на админа
# class IsAdmin(BaseFilter):
#     def __init__(self, admin_ids: list[int]) -> None:
#         # В качестве параметра фильтр принимает список с целыми числами
#         self.admin_ids = admin_ids
#
#     async def __call__(self, message: Message) -> bool:
#         return message.from_user.id in self.admin_ids


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Доброго дня! Вас вітає бот крамниць «Копілочка» - зручний помічник для здійснення покупок.'
             ' Будь ласка, поділіться Вашим номером телефону для отримання акцій.',
        reply_markup=keyboard_start
    )


# Этот хэндлер будет срабатывать на блокировку бота пользователем
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    results = select_users(path_sqlite, event.from_user.id)
    if results:
        update_users(path_sqlite, False, event.from_user.id)


# Этот хэндлер будет срабатывать на команду поделиться контаком
@router.message(F.contact)
async def send_tel(message: Message):
    # print(message.contact)
    # print(message.from_user)
    if message.from_user.id == message.contact.user_id:
        results = select_users(path_sqlite, message.from_user.id)
        if results:
            update_users(path_sqlite, True, message.from_user.id)
        else:
            add_users(path_sqlite,
                      message.from_user.id,
                      message.contact.first_name,
                      message.contact.phone_number,
                      True
                      )
        await message.answer(
            text='Головне меню',
            reply_markup=keyboard_inline
        )
    else:
        await message.answer(
            text='Натисніть поділитися контактом',
            reply_markup=keyboard_start
        )


# Хэндлер на команду акции
@router.callback_query(F.data == "button_stock_clik")
async def send_random_value(callback: CallbackQuery):
    image_from_pc = FSInputFile(path_img_sale)
    await callback.message.answer_photo(
        image_from_pc,
        caption="Акція")
    await callback.message.answer(text='Головне меню',
                                  reply_markup=keyboard_inline)
    await callback.answer()


# Хэндлер на команду кубик
@router.callback_query(F.data == "button_dice_clik")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer_dice(emoji="🎲")
    await callback.message.answer(text='Головне меню', reply_markup=keyboard_inline)
    await callback.answer()


# Хэндлер на команду баскетбол
@router.callback_query(F.data == "button_basketball_clik")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer_dice(emoji="🏀")
    await callback.message.answer(text='Головне меню', reply_markup=keyboard_inline)
    await callback.answer()


# Этот хэндлер будет срабатывать, если апдейт от админа
@router.message(IsAdmin(admin_ids_list), F.text.lower() == 'send')
async def answer_if_admins_update(message: Message):
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    results = select_active_users(path_sqlite)
    image_from_pc = FSInputFile(path_img_sale)
    for user in results:
        try:
            await bot.send_photo(user[0], image_from_pc, caption="Акція")
        except:
            pass
        # await message.send_copy()
        # await message.send_copy(chat_id=message.chat.id)
        # await bot.send_photo(user[0], image_from_pc)
        # await message.answer_photo(
        #     image_from_pc,
        #     caption="Акція",
        #     use)
    # await message.answer(text='Вы админ')
