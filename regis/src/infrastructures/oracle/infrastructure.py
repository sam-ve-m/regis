from contextlib import asynccontextmanager

import cx_Oracle_async
from etria_logger import Gladsheim

from regis.src.domain.exceptions.infrastructure import ErrorToStartInfrastructure
from regis.src.infrastructures.env_config import config


class OracleInfrastructure:
    pool = None

    @classmethod
    def _get_configs(cls) -> dict:
        return {
            "host": config("REGIS_ORACLE_BASE_DSN"),
            "port": config("REGIS_ORACLE_PORT"),
            "user": config("REGIS_ORACLE_USER"),
            "password": config("REGIS_ORACLE_PASSWORD"),
            "service_name": config("REGIS_ORACLE_SERVICE"),
        }

    @classmethod
    async def _get_pool(cls):
        if cls.pool is None:
            connectio_config = cls._get_configs()
            try:
                cls.pool = await cx_Oracle_async.create_pool(
                    host=connectio_config["host"],
                    port=connectio_config["port"],
                    user=connectio_config["user"],
                    password=connectio_config["password"],
                    service_name=connectio_config["service_name"],
                    min=2,
                    max=4,
                )
            except Exception as exception:
                Gladsheim.error(
                    message=f"""{cls.__name__}::_get_pool::Error on pool connection for the credentials 
                    host={connectio_config["host"]} 
                    port={connectio_config["port"]} 
                    user={connectio_config["user"]} 
                    service_name={connectio_config["service_name"]}:  
                    {exception}""",
                    error=exception,
                )
                raise ErrorToStartInfrastructure("Ops! Fail to connect!!!")
        return cls.pool

    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        pool = await cls._get_pool()
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    yield cursor
        except Exception as exception:
            Gladsheim.error(
                message=f"""{cls.__name__}::get_connection::Error getting cursor""",
                error=exception,
            )
            raise exception
