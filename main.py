import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

# from middlewares.user_availability import UserAvailabilityMiddleware

from config import Config

from handlers.start import router as command_router
from handlers.context import router as context_router
from handlers.requests import router as requests_router
from handlers.histories import router as histories_router

from repositories.realizations import redis
from repositories import Repository
from services import Service


logging.basicConfig(level=logging.INFO)


def register_routers(dp: Dispatcher):
    dp.include_router(command_router)
    dp.include_router(context_router)
    dp.include_router(histories_router)
    dp.include_router(requests_router)


# def register_middlewares(dp: Dispatcher):
#     dp.update.outer_middleware(UserAvailabilityMiddleware(dp['repository'].users))


async def register_default_commands(dp: Dispatcher):
    command_list = []
    for key in dp['commands']:
        command_list.append(BotCommand(command=key[1:], description=dp['commands'][key]))

    await dp['bot'].set_my_commands(command_list)


# def on_first_startup(repository: Repository):
#     from repositories.mysql.models import Base
#     Base.metadata.drop_all(repository.engine)
#     Base.metadata.create_all(repository.engine)


async def main():
    config = Config()
    bot = Bot(config.bot.token, parse_mode='Markdown')

    # mysql_engine = mysql.get_engine(config.mysql)
    redis_engine = redis.get(config.redis)

    repository = Repository(config, None, redis_engine)
    service = Service(repository)

    repository.histories.clear(587247376)

    dp = Dispatcher(storage=MemoryStorage())
    
    dp['config'] = config
    dp['dp'] = dp
    dp['bot'] = bot
    dp['service'] = service

    # dp['repository'] = repository

    dp['commands'] = {"/context": "Установить контекст"}
    
    # on_first_startup(repository)

    await register_default_commands(dp)
    
    register_routers(dp)
    # register_middlewares(dp)

    await dp.start_polling(dp['bot'])


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
