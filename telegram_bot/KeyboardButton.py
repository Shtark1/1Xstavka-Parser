from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


btn_total_yew = KeyboardButton("Тотал жёлтых")
btn_gen_total = KeyboardButton("Общий тотал по очкам")
btn_add_admin = KeyboardButton("Добавить пользователя")
btn_cancel = KeyboardButton("Отмена")

BUTTON_TYPES = {
    "BTN_HOME": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_total_yew).add(btn_gen_total),
    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_total_yew).add(btn_gen_total).add(btn_add_admin),
    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)

}
