import logging
import markdown

from models import Promt, PromtRole
import repositories
from ..interfaces import OpenAI


class OpenAIService(OpenAI):
    def __init__(self, openai_repository: repositories.OpenAI, histories_repository: repositories.Histories):
        self.histories_repository: repositories.Histories = histories_repository
        self.openai_repository: repositories.OpenAI = openai_repository

    async def make_request(self, user_id: int, text: str) -> str:
        promt = Promt(PromtRole.user, text)
        self.histories_repository.add(user_id, promt)
        promts = self.histories_repository.get(user_id)
        logging.info(promts)

        try:
            response = await self.openai_repository.make_request(promts)

        except Exception as error:
            response = str(error) + " - error!"

        else:
            self.histories_repository.add(user_id, response)
            response = response.value
            response = response.replace('*', '\\*')
            response = response.replace('_', '\\_')
            
        logging.info(response + "\n")


        return response
        
    def get_context(self, user_id: int) -> str|None:
        history = self.histories_repository.get(user_id)
        
        if self.check_context(history):
            return history[0].value
        
        return None
            
    def set_context(self, user_id: int, text: str):
        context = Promt(PromtRole.system, text)
        history = self.histories_repository.get(user_id)

        if self.check_context(history):
            history[0] = context
        else:
            history = [context] + history

        self.update_history(user_id, history)

    def delete_context(self, user_id: int):
        history = self.histories_repository.get(user_id)

        if self.check_context(history):
            history = history[1:]
            self.update_history(user_id, history)

    def clear_history(self, user_id: int):
        history = self.histories_repository.get(user_id)

        if self.check_context(history):
            history = history[0:1]
        else:
            history = []
        
        self.update_history(user_id, history)

    def clear_history_with_context(self, user_id: int):
        self.histories_repository.clear(user_id)

    @staticmethod
    def check_context(history: list[Promt]) -> bool:
        if len(history) == 0:
            return False
        
        if history[0].role != PromtRole.system:
            return False
        
        return True
    
    def update_history(self, user_id: int, history: list[Promt]):
        self.histories_repository.clear(user_id)

        for promt in history:
            self.histories_repository.add(user_id, promt)

    