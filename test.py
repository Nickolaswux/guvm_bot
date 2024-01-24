import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

from tokenbot import TOKONBOT, MESSAGE_GROUP, TOKONBOT_POST
from keyboards_serv import key_s

token = TOKONBOT
token2 = TOKONBOT_POST
group_id = MESSAGE_GROUP

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

bot2 = Bot(token=token2, parse_mode='HTML')
dp2 = Dispatcher(bot2, storage=MemoryStorage())

async def on_startup(dp):
    logging.warning('Starting bot 1...')
    await bot.send_message(chat_id=group_id, text='Bot 1 has been started')

async def on_startup2(dp):
    logging.warning('Starting bot 2...')
    await bot2.send_message(chat_id=group_id, text='Bot 2 has been started')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Bot 1: Choose a language / Выберите язык", reply_markup=key_s["lang_key"])

@dp2.message_handler(commands=['start'])
async def start_command2(message: types.Message):
    await message.answer("Bot 2: Choose a language / Выберите язык", reply_markup=key_s["lang_key"])

async def main():
    # Создаем задачи для асинхронного запуска обоих ботов
    tasks = [
        dp.start_polling(),
        dp2.start_polling()
    ]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()

    # Запускаем основную задачу
    loop.run_until_complete(main())
    loop.run_forever()