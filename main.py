from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from create_bot import dp
from telegram_bot import Admin, Client


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def main():
    Admin.register_handler_admin(dp)
    Client.register_handler_client(dp)

    executor.start_polling(dp, on_shutdown=shutdown)


if __name__ == '__main__':
    main()
    