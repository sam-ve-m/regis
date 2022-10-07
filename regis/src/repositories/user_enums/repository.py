from hashlib import sha1

import orjson as json
from etria_logger import Gladsheim

from regis.src.domain.exceptions.repository import FailedToVerifyEnum
from regis.src.infrastructures.redis import RedisInfrastructure


class UserEnumsRepository(RedisInfrastructure):
    @classmethod
    async def is_the_city_in_frontier(cls, code: int) -> bool:
        # TODO: change this query to get the real value
        sql = f"""
            SELECT NOME_MUNI
            FROM CORRWIN.TSCDXMUNICIPIO
            WHERE NUM_SEQ_MUNI = :code
        """
        tuple_result = False
        # tuple_result = await cls._query_with_cache(sql=sql, values={"code": code})
        # if tuple_result:
        #     return tuple_result[0][0]
        return bool(tuple_result)

    @classmethod
    async def is_the_profession_risk(cls, code: int) -> bool:
        # TODO: change this query to get the real value
        sql = f"""
            SELECT DESCRIPTION
            FROM USPIXDB001.SINCAD_EXTERNAL_PROFESSIONAL
            WHERE CODE = :code
        """

        tuple_result = False
        # tuple_result = await cls._query_with_cache(sql=sql, values={"code": code})
        # if tuple_result:
        #     return tuple_result[0][0]
        return bool(tuple_result)

    # @classmethod
    # async def _query_with_cache(cls, sql: str, values: dict) -> list:
    #     try:
    #         partial_key = cls.__encode_query(sql=sql, values=values)
    #         redis = cls._get_client()
    #         key = f"regis:{partial_key}"
    #         value = await redis.get(key)
    #         if not value:
    #             partial_value = await cls._query(sql=sql, values=values)
    #             value = {"value": partial_value}
    #             await redis.set(name=key, value=json.dumps(value), ex=3600)
    #             return partial_value
    #         value = json.loads(value)
    #         value = value.get("value")
    #         return value
    #     except FailedToVerifyEnum as error:
    #         raise error
    #     except Exception as error:
    #         Gladsheim.error(
    #             message=f"{cls.__name__}::_query_with_cache::Failed to get data",
    #             error=error,
    #         )
    #         raise FailedToVerifyEnum()
    #
    # @classmethod
    # async def _query(cls, sql: str, values: dict) -> list:
    #     try:
    #         async with cls.get_connection() as cursor:
    #             await cursor.execute(sql, values)
    #             rows = await cursor.fetchall()
    #             return rows
    #     except Exception as error:
    #         Gladsheim.error(
    #             message=f"{cls.__name__}::_query::Failed to execute query",
    #             sql=sql,
    #             parameters=values,
    #             error=error,
    #         )
    #         raise FailedToVerifyEnum()
    #
    # @staticmethod
    # def __encode_query(sql: str, values: dict):
    #     _sha1 = sha1()
    #     _sha1.update((str(sql) + str(values)).encode())
    #     encoded_key = _sha1.hexdigest()
    #     return encoded_key
