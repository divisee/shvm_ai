import asyncio
# import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.users_handler import router
from config import BOT_TOKEN

async def main():
    # Создание экземпляра бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация маршрутизатора
    dp.include_router(router)

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
