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
    bot_message = await message.answer("⌛ *Посылаем запрос на сервера...*")

    task = asyncio.create_task(send_wait_messages(bot_message))
    response = await service.openai.make_request(message.from_user.id, message.text)
    task.cancel()
    
    await bot_message.edit_text(response)


async def send_wait_messages(message: Message):
    texts = [
        "⌛ *Сервера включают видеокарты...*",
        "⌛ *Нейронные сети определяются с ответом...*",
        "⌛ *Ждем ответ от серверов...*",
        "⌛ *Обрабатываем ответ...*"
        ]
    
    while True:
        for text in texts:
            await sleep(1)
            await message.edit_text(text)
