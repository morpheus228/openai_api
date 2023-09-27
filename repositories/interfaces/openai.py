from abc import ABC, abstractmethod

from models import Promt


class OpenAI(ABC):
    @abstractmethod
    async def make_request(self, promts: list[Promt]) -> Promt:
        pass