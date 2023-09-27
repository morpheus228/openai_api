from redis import StrictRedis

from models import Promt, PromtRole
from repositories.interfaces import Histories


class HistoriesRedis(Histories):
    def __init__(self, redis: StrictRedis):
        self.redis: StrictRedis = redis
        self.prefix: str = "HISTORIES"
    
    def add(self, user_id: int, promt: Promt):
        self.redis.rpush(self.key(user_id), self.encode_promt(promt))

    def clear(self, user_id: int):
        self.redis.delete(self.key(user_id))

    def get(self, user_id: int) -> list[Promt]:
        promts = self.redis.lrange(self.key(user_id), 0, -1)
        return [self.decode_promt(promt) for promt in promts]

    def key(self, user_id: int) -> str:
        return f"{self.prefix}:{user_id}"
    
    @staticmethod
    def encode_promt(promt: Promt) -> str:
        return f"{str(promt.role)}:{promt.value}"

    @staticmethod
    def decode_promt(promt: bytes) -> Promt:
        tmp = promt.decode("utf-8").split(":")
        return Promt(PromtRole(tmp[0]), ":".join(tmp[1:]))


