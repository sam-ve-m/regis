from hashlib import sha1
from typing import Tuple

import orjson as json
from etria_logger import Gladsheim

from regis.src.domain.exceptions.repository import FailedToGetData
from regis.src.infrastructures.oracle.infrastructure import OracleInfrastructure
from regis.src.infrastructures.redis import RedisInfrastructure


class UserEnumsRepository(OracleInfrastructure, RedisInfrastructure):
    @classmethod
    async def is_the_city_in_frontier(cls, city_code: int) -> bool:
        city = await cls.get_city_by_code(code=city_code)
        is_in_frontier = await cls.verify_if_the_city_is_in_frontier(
            city_name=city[0], state=city[1]
        )
        return is_in_frontier

    @classmethod
    async def is_the_profession_risky(cls, code: int) -> bool:
        sql = f"""
            SELECT RISK
            FROM USPIXDB001.SINCAD_EXTERNAL_PROFESSIONAL
            WHERE CODE = :code
        """
        tuple_result = await cls._query_with_cache(sql=sql, values={"code": code})
        if tuple_result:
            return bool(tuple_result[0][0])
        return bool(tuple_result)

    @classmethod
    async def get_city_by_code(cls, code: int) -> Tuple[str, str]:
        sql = f"""
            SELECT NOME_MUNI, SIGL_ESTADO
            FROM CORRWIN.TSCDXMUNICIPIO
            WHERE NUM_SEQ_MUNI = :code
        """

        tuple_result = await cls._query_with_cache(sql=sql, values={"code": code})
        if tuple_result:
            return tuple_result[0]
        else:
            raise FailedToGetData()

    @classmethod
    async def verify_if_the_city_is_in_frontier(
        cls, city_name: str, state: str
    ) -> bool:
        sql = f"""
            SELECT 1
            FROM USPIXDB001.FRONTIER_CITIES
            WHERE NOME_MUNI = :city_name
            AND SIGL_ESTADO = :state
        """
        tuple_result = await cls._query_with_cache(
            sql=sql,
            values={
                "city_name": city_name,
                "state": state,
            },
        )
        if tuple_result:
            return bool(tuple_result[0])
        return bool(tuple_result)

    @classmethod
    async def _query_with_cache(cls, sql: str, values: dict) -> list:
        try:
            partial_key = cls.__encode_query(sql=sql, values=values)
            redis = cls._get_client()
            key = f"regis:{partial_key}"
            value = await redis.get(key)
            if not value:
                partial_value = await cls._query(sql=sql, values=values)
                value = {"value": partial_value}
                await redis.set(name=key, value=json.dumps(value), ex=3600)
                return partial_value
            value = json.loads(value)
            value = value.get("value")
            return value
        except FailedToGetData as error:
            raise error
        except Exception as error:
            Gladsheim.error(
                message=f"{cls.__name__}::_query_with_cache::Failed to get data",
                error=error,
            )
            raise FailedToGetData()

    @classmethod
    async def _query(cls, sql: str, values: dict) -> list:
        try:
            async with cls.get_connection() as cursor:
                await cursor.execute(sql, values)
                rows = await cursor.fetchall()
                return rows
        except Exception as error:
            Gladsheim.error(
                message=f"{cls.__name__}::_query::Failed to execute query",
                sql=sql,
                parameters=values,
                error=error,
            )
            raise FailedToGetData()

    @staticmethod
    def __encode_query(sql: str, values: dict):
        _sha1 = sha1()
        _sha1.update((str(sql) + str(values)).encode())
        encoded_key = _sha1.hexdigest()
        return encoded_key
