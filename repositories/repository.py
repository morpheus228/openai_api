from redis import StrictRedis

from config import Config

from .realizations import *
from .interfaces import *


class Repository:
	def __init__(self, config: Config, mysql_engine, redis: StrictRedis):
		# self.mysql_engine = mysql_engine
		self.config: Config = config
		self.redis: StrictRedis = redis
		
		self.openai: OpenAI = OpenAIRepository(config.openai)
		# self.users: Users = UsersMYSQL(mysql_engine)
		self.histories: Histories = HistoriesRedis(redis)

