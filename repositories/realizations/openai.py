import logging
import httpx
import copy

from dataclasses import dataclass
from strenum import StrEnum

from config import OpenAIConfig
from errors import OpenAIRequestError, OpenAIRequestTimeoutError
from models import Promt, PromtRole
from utils.logging import log_time
from ..interfaces import OpenAI


class Models(StrEnum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"


@dataclass
class Settings:
    max_tokens: int = 1000
    temperature: float = 1
    top_p: float = 1



class OpenAIRepository(OpenAI):
    def __init__(self, config: OpenAIConfig, settings: Settings = Settings()):
        self.url: str = "https://api.openai.com/v1/chat/completions"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.token}"
            }
        
        self.data = {
            "model": "gpt-3.5-turbo",
            "messages": None,
            "max_tokens": 1000,
            "temperature": 1,
            "top_p": 1
        }
        
        self.model: str = config.model
        self.timeout: float = 120
    
    @staticmethod
    def encode_input(promts: list[Promt]) -> list[dict[str, str]]:
        return [{"role": str(promt.role), "content": promt.value} for promt in promts]

    async def make_request(self, promts: list[Promt]) -> Promt:
        data = copy.deepcopy(self.data)
        data['messages'] = self.encode_input(promts)
        
        try:
            response = await self.post(data)

        except httpx.ReadTimeout:
            raise OpenAIRequestTimeoutError
        
        except Exception as err:
            raise OpenAIRequestError(str(err))
        
        if response.status_code == 400:
            raise OpenAIRequestError(response.json())
        
        try:
            logging.info(response.json())
            message = response.json()['choices'][0]['message']['content']
            return Promt(PromtRole.assistant, message)
        
        except Exception as err:
            raise OpenAIRequestError(str(err))

    @log_time
    async def post(self, data: dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.post(self.url, headers=self.headers, json=data, timeout=self.timeout)
