from abc import ABC, abstractmethod

class OpenAI(ABC):
    @abstractmethod
    async def make_request(self, user_id: int, text: str) -> str:
        pass

    @abstractmethod
    def get_context(self, user_id: int) -> str|None:
        pass

    @abstractmethod     
    def set_context(self, user_id: int, text: str):
        pass

    @abstractmethod
    def delete_context(self, user_id: int):
        pass

    @abstractmethod
    def clear_history(self, user_id: int):
       pass

    @abstractmethod
    def clear_history_with_context(self, user_id: int):
        pass