from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass
class BotConfig:
    token: str
    # admin_ids: list

@dataclass
class OpenAIConfig:
    token: str
    model: str

@dataclass
class MYSQLConfig:
    host: str
    password: str
    user: str
    database: str
    port: str

@dataclass
class RedisConfig:
    host: str
    password: str
    database: int
    port: int


@dataclass
class Config:
    bot: BotConfig
    openai: OpenAIConfig
    mysql: MYSQLConfig
    redis: RedisConfig

    def __init__(self):
        load_dotenv('.env')
        
        self.bot = BotConfig(
            token=os.getenv("BOT_TOKEN"))

        self.openai = OpenAIConfig(
            token=os.getenv("OPENAI_TOKEN"),
            model=os.getenv("OPENAI_MODEL"))

        self.mysql = MYSQLConfig(
            host=os.getenv('MYSQL_HOST'),
            password=os.getenv('MYSQL_PASSWORD'),
            user=os.getenv('MYSQL_USER'),
            database=os.getenv('MYSQL_DATABASE'),
            port=os.getenv('MYSQL_PORT'))
            
        self.redis = RedisConfig(
            host=os.getenv('REDIS_HOST'),
            password=os.getenv('REDIS_PASSWORD'),
            database=int(os.getenv('REDIS_DATABASE')),
            port=int(os.getenv('REDIS_PORT')))