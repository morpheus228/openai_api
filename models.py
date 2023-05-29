import openai as openai
from environs import Env

env = Env()
env.read_env('.env')
openai.api_key = env.str('OPENAI_TOKEN')


class ChatModel:
    def __init__(self, model: str, max_tokens: int = 1000, temperature: float = 1, top_p: float = 1):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

    def make_request(self, user_content: str, system_content: str = None, assistant_content: str = None) -> str:
        messages = [{"role": "user", "content": user_content}]

        if system_content is not None:
            messages.append({"role": "system", "content": system_content})

        if assistant_content is not None:
            messages.append({"role": "assistant", "content": assistant_content})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                max_tokens=self.max_tokens,

                temperature=self.temperature,
                top_p=self.top_p,

                messages=messages
            )
            return response.choices[0].message.content

        except openai.error.RateLimitError or openai.error.InvalidRequestError as error:
            return error
