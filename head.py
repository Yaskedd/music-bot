import asyncio
import logging
import sys
from os import getenv

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot_instance import bot
from handlers.routes import router
from middlewares.subscription import SubscriptionMiddleware

load_dotenv()
TOKEN = getenv('BOT_TOKEN')
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)
dispatcher.include_router(router)
dispatcher.message.middleware(SubscriptionMiddleware())


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Бот запускается...")
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
'''
подключаем наш класс к диспечеру,который буквально говорит:
 "Перед запуском любого handler'а возьми пользователя, проверь его подписку.
Если он не подписан — покажи кнопку подписки и остановись. Если подписан — передай событие дальше handler'у"
'''
