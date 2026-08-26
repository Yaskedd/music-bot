import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from handlers.routes import router
from bot_instance import bot

load_dotenv()
TOKEN = getenv('BOT_TOKEN')
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)
dispatcher.include_router(router) 

async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("Бот запускается...")
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())