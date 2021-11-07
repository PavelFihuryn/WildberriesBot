import os
from asyncio import sleep

import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command, RegexpCommandsFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import json

from config import ADMIN_ID
from main import bot, dp, base, conn
from parser import get_brand, get_title


# ADMIN_ID = os.environ["ADMIN_ID"]


def user_id(message):
    return message['from']['id']


async def send_to_admin(dp):
    await bot.send_message(
        chat_id=ADMIN_ID,
        text="Бот запущен",
    )


@dp.message_handler(Command("start"))
async def start_bot(message: Message):
    await bot.send_message(
        chat_id=user_id(message),
        text="Привет! Я могу по артикулу товара в каталоге Wildberries назвать бренд и его название.\n"
             "Узнать бренд - /get_brand 12345678\n"
             "Узнать название - /get_title 12345678\n",
    )


@dp.message_handler(RegexpCommandsFilter(regexp_commands=['get_brand ([0-9]*)']))
async def get_brand_message(message: Message, regexp_command):
    code = regexp_command.group(1)
    text = get_brand(code)
    await message.answer(text=text)


@dp.message_handler(RegexpCommandsFilter(regexp_commands=['get_title ([0-9]*)']))
async def get_title_message(message: Message, regexp_command):
    code = regexp_command.group(1)
    text = get_title(code)
    await message.answer(text=text)


@dp.message_handler()
async def echo(message: Message):
    text = f"Команда {message.text} не известна. Команда должна быть вида /get_brand 12345678 или /get_title 12345678."
    await message.answer(text=text)


def save_in_db(code, json_data):
    base.execute("INSERT INTO products(product_id, product_info) VALUES (?, ?)", (code, json.dumps(json_data)))
    conn.commit()


@dp.message_handler(Command("save"))
async def save_json(message: Message):
    code = '123456'
    json_data = requests.get('https://api.telegram.org/bot2140818186:AAG9y0XUavyf6cItnkkqpxAEbMiPdneHpoE/getMe')
    save_in_db(code, json_data.json())
