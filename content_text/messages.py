from telegram_bot.utils import StatesUsers

# СООБЩЕНИЯ ОТ БОТА
stat_message = """Привет 👋

Ты попал в бота для парсинга 1xставка"""
stat_no = "У табя нет доступа к этому боту, пиши сюда https://t.me/henqsi"
start_admin_message = "Приветствую админ 👋"
not_command_message = "Такой команды нет"

add_admin_message = """ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""
not_admin_id_message = """Это не число, ID состоит только из чисел, его можно получить тут https://t.me/getmyid_bot
Вводи ID пользователя:"""


MESSAGES = {
    "start": stat_message,
    "start_no": stat_no,
    "start_admin": start_admin_message,
    "not_command": not_command_message,
    "add_admin": add_admin_message,
    "not_admin_id": not_admin_id_message,

}
