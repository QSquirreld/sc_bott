import os
from dotenv import load_dotenv
from handlers import router
import asyncio
from aiogram import Bot, Dispatcher

load_dotenv()

bot = Bot(token=os.getenv('TG_BOT_TOKEN'))
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
