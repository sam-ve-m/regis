import redis.asyncio as redis
from etria_logger import Gladsheim
from redis.asyncio import Redis

from regis.src.domain.exceptions.infrastructure import (
    ErrorToStartInfrastructure,
)
from regis.src.infrastructures.env_config import config


class RedisInfrastructure:
    redis = None

    @classmethod
    def _get_client(cls) -> Redis:
        redis_url = config("REGIS_REDIS_URL")
        if cls.redis is None:
            try:
                cls.redis = redis.from_url(redis_url, health_check_interval=0)
            except Exception as e:
                Gladsheim.error(
                    message=f"{cls.__name__}::_get_client::Error on client connection for the giving url",
                    error=e,
                )
                raise ErrorToStartInfrastructure()
        return cls.redis
