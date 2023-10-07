from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services import Service

from utils.message_template import MessageTemplate

router = Router()


@router.message(Command('reset'))
async def reset(message: Message, state: FSMContext, service: Service):    
    service.openai.clear_history(message.from_user.id)
    text, reply_markup = MessageTemplate.from_json('histories/reset').render()
    await message.answer(text=text, reply_markup=reply_markup)


