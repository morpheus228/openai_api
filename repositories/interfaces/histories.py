from abc import ABC, abstractmethod

from models import Promt



class Histories(ABC):
    @abstractmethod
    def add(self, user_id: int, promt: Promt):
        pass

    @abstractmethod
    def clear(self, user_id: int):
        pass

    @abstractmethod
    def get(self, user_id: int) -> list[Promt]:
        pass