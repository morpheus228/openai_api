from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.message_template import MessageTemplate
from services import Service


class States(StatesGroup):
    context = State()

router = Router()


@router.message(Command('context'))
async def context(message: Message, service: Service):
    context = service.openai.get_context(message.from_user.id)
    context = context if context is not None else "---"
    text, reply_markup = MessageTemplate.from_json('context/context').render(context=context)
    await message.answer(text=text, reply_markup=reply_markup)


@router.callback_query(F.data == "delete_context")
async def delete_context(call: CallbackQuery, state: FSMContext, service: Service):
    service.openai.delete_context(call.from_user.id)
    text, reply_markup = MessageTemplate.from_json('context/success_delete').render(context=context)
    await call.message.edit_text(text, reply_markup=reply_markup)


@router.callback_query(F.data == "change_context")
async def request_context(call: CallbackQuery, state: FSMContext):
    text, reply_markup = MessageTemplate.from_json('context/request').render(context=context)
    await call.message.edit_text(text, reply_markup=reply_markup)
    await state.set_state(States.context)


@router.message(States.context)
async def accept_context(message: Message, service: Service, state: FSMContext):
    service.openai.set_context(message.from_user.id, message.text)
    text, reply_markup = MessageTemplate.from_json('context/success_change').render(context=context)
    await message.answer(text, reply_markup=reply_markup)
    await state.clear()
    