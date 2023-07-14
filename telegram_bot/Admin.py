from aiogram.types import Message
from aiogram.dispatcher import FSMContext, Dispatcher

from telegram_bot.utils import StatesAdmin
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.config import ADMIN_ID
from create_bot import dp, bot


# ===================================================
# ===================== АДМИНКА =====================
# ===================================================
# ================= ДОБАВИТЬ АДМИНА =================
async def add_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[1])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"], reply_markup=BUTTON_TYPES["BTN_HOME"])


# =============== ВВОД ID АДМИНА ===============
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        ADMIN_ID.append(new_users_id)
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(add_admin, lambda message: message.text.lower() == 'добавить пользователя')
    dp.register_message_handler(id_admin, state=StatesAdmin.STATES_1)

