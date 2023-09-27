import asyncio
from typing import Coroutine
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from anyio import sleep
from services.service import Service

from utils.message_template import MessageTemplate

router = Router()


@router.message(F.text != None)
async def request(message: Message, service: Service):
    bot_message = await message.answer("<b>Посылаем запрос на сервера...</b>")
    # task = asyncio.create_task(send_wait_messages(message))
    response = await service.openai.make_request(message.from_user.id, message.text)
    # print(response)
    # task.cancel()
    await bot_message.edit_text(response)


async def send_wait_messages(message: Message):
    texts = [
        "<b>Сервера включают видеокарты...</b>",
        "<b>Нейронные сети определяются с ответом...</b>",
        "<b>Ждет ответа от серверов...</b>",
        "<b>Обрабатываем ответ...</b>"
        ]
    
    while True:
        print('ddffdf')
        for text in texts:
            sleep(0.5)
            await message.edit_text(text)
