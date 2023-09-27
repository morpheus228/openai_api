from config import Config
from repositories import Repository

from .realizations import *
from .interfaces import *


class Service:
	def __init__(self, repository: Repository):
		self.openai: OpenAI = OpenAIService(repository.openai, repository.histories)
