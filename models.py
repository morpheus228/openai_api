from dataclasses import dataclass
from strenum import StrEnum


class PromtRole(StrEnum):
    user = "user"
    system = "system"
    assistant = "assistant"


@dataclass
class Promt:
    role: PromtRole
    value: str

