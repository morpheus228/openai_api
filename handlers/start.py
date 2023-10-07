from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.message_template import MessageTemplate

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):    
    kwargs = {"first_name": message.from_user.first_name}
    text, reply_markup = MessageTemplate.from_json('commands/start').render(**kwargs)
    await message.answer(text=text, reply_markup=reply_markup)


