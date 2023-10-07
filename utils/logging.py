import time
import logging


def log_time(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time
        logging.info(f"OpenAI request was completed in {round(execution_time, 2)} seconds. {result.status_code}.")
        return result
    return wrapper