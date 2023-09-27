from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.message_template import MessageTemplate

router = Router()


@router.message(Command('set_context'))
async def context(message: Message, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('context/context').render()
    await message.answer(text=text, reply_markup=reply_markup)