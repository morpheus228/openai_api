from redis import StrictRedis

from config import RedisConfig


def get(config: RedisConfig) -> StrictRedis:
	return StrictRedis(host=config.host, port=config.port, db=config.database)

