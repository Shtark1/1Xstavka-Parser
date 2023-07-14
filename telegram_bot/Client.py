import asyncio
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ContentTypes
from aiogram.dispatcher import FSMContext, Dispatcher

from telegram_bot.KeyboardButton import BUTTON_TYPES
from telegram_bot.utils import StatesUsers
from content_text.messages import MESSAGES
from cfg.config import ADMIN_ID, USER_ID
from create_bot import dp, bot
from Parser.MainParser import start_pars


# ===================================================
# =============== СТАНДАРТНЫЕ КОМАНДЫ ===============
# ===================================================
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID or message.from_user.id in USER_ID:
        await bot.send_message(text=MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"], chat_id=message.from_user.id)
    else:
        await bot.send_message(text=MESSAGES["start_no"], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)


# ====================================================
# =================== ВЫВОД ТОПОВ ====================
# ====================================================
async def gen_total_match(message: Message):
    if message.from_user.id in ADMIN_ID or message.from_user.id in USER_ID:
        await bot.send_message(text="Введи конкретный тотал", reply_markup=BUTTON_TYPES["BTN_CANCEL"], chat_id=message.from_user.id)
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what=message.text)
        await state.set_state(StatesUsers.all()[0])
    else:
        await bot.send_message(text=MESSAGES["start_no"], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)


async def gen_total_match_2(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
        await state.finish()
    elif message.text.isnumeric():
        what = await state.get_data()
        await start_pars(message, 100, what["what"])
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer("Это не число попробуй снова", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesUsers.all()[0])


async def yellow_total_match(message: Message):
    if message.from_user.id in ADMIN_ID or message.from_user.id in USER_ID:
        await bot.send_message(text="Введи конкретный тотал", reply_markup=BUTTON_TYPES["BTN_CANCEL"], chat_id=message.from_user.id)
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what=message.text)
        await state.set_state(StatesUsers.all()[1])
    else:
        await bot.send_message(text=MESSAGES["start_no"], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)


async def yellow_total_match_2(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME"])
        await state.finish()
    elif message.text.isnumeric():
        what = await state.get_data()
        await start_pars(message, 100, what["what"])
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer("Это не число попробуй снова", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesUsers.all()[0])


# ===================================================
# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
# ===================================================
async def unknown_command(message: Message):
    if message.from_user.id in ADMIN_ID or message.from_user.id in USER_ID:
        await bot.send_message(text=MESSAGES['not_command'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"], chat_id=message.from_user.id)
    else:
        await bot.send_message(text=MESSAGES["start_no"], reply_markup=BUTTON_TYPES["BTN_HOME"], chat_id=message.from_user.id)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")

    dp.register_message_handler(gen_total_match, lambda message: message.text.lower() == 'общий тотал по очкам')
    dp.register_message_handler(gen_total_match_2, state=StatesUsers.STATE_0)

    dp.register_message_handler(yellow_total_match, lambda message: message.text.lower() == 'тотал жёлтых')
    dp.register_message_handler(yellow_total_match_2, state=StatesUsers.STATE_1)

    dp.register_message_handler(unknown_command, content_types=["text"])
