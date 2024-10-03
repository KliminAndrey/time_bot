from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import logging
import asyncio

from config_data.config import load_config
config = load_config()
BOT_TOKEN = config.tg_bot.token

sched = AsyncIOScheduler(timezone="Asia/Yekaterinburg")
logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЗадай напоминание в формате ЧЧ.ММ ДД.ММ.ГГГГ <текст напоминания>')


async def remind(user_id, text):
    await bot.send_message(user_id, text)


@dp.message()
async def get_task(message: Message):

    text_task = (message.text)[16:]
    hour = (int)(message.text[:2])
    minute = (int)(message.text[3:5])
    day = (int)(message.text[6:8])
    month = (int)(message.text[9:11])
    year = (int)(message.text[12:16])
    time = datetime(year, month, day, hour, minute)
    sched.add_job(remind, "date", args=[message.from_user.id, text_task], run_date=time)
    await message.reply("ok")






async def main():
    sched.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())