from unittest.mock import patch, AsyncMock

import decouple
import pytest
from etria_logger import Gladsheim

from regis.src.domain.exceptions.repository import FailedToGetData
from regis.src.repositories.user_enums.repository import UserEnumsRepository


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "_query_with_cache")
async def test_get_city_by_code(query):
    query.return_value = [("city", "state")]
    result = await UserEnumsRepository.get_city_by_code(code=0)
    assert result == ("city", "state")


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "_query_with_cache")
async def test_get_city_by_code_when_result_is_empty(query):
    query.return_value = []
    with pytest.raises(FailedToGetData):
        result = await UserEnumsRepository.get_city_by_code(code=0)


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "_query_with_cache")
async def test_is_the_profession_risky_when_is_risky(query):
    query.return_value = [(1,)]
    result = await UserEnumsRepository.is_the_profession_risky(code=0)
    assert result == True


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "_query_with_cache")
async def test_is_the_profession_risky_when_is_not_risky(query):
    query.return_value = [(0,)]
    result = await UserEnumsRepository.is_the_profession_risky(code=0)
    assert result == False


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "get_city_by_code", return_value=["SAO PAULO", "SP"])
@patch.object(UserEnumsRepository, "verify_if_the_city_is_in_frontier", return_value=False)
async def test_is_the_city_in_frontier(get_city, verify_city):
    result = await UserEnumsRepository.is_the_city_in_frontier(city_code=0)
    assert result == False
    assert get_city.called


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "_query_with_cache")
async def test_verify_if_the_city_is_in_frontier_when_city_is_in_frontier(query):
    query.return_value = [(1,)]
    result = await UserEnumsRepository.verify_if_the_city_is_in_frontier(city_name="SAO PAULO", state="SP")
    assert result == True


@pytest.mark.asyncio
@patch.object(UserEnumsRepository, "_query_with_cache")
async def test_verify_if_the_city_is_in_frontier_when_city_is_not_in_frontier(query):
    query.return_value = []
    result = await UserEnumsRepository.verify_if_the_city_is_in_frontier(city_name="SAO PAULO", state="SP")
    assert result == False


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserEnumsRepository, "_query")
@patch.object(UserEnumsRepository, "_get_client")
async def test__query_with_cache_when_there_is_cache(redis_client, query, error):
    query_cache_result = '{"value": [["city", "city_code"]]}'
    redis_client_mock = AsyncMock()
    redis_client_mock.get.return_value = query_cache_result
    redis_client.return_value = redis_client_mock
    result = await UserEnumsRepository._query_with_cache(sql="SQL", values={"id": 10})
    expected_result = [["city", "city_code"]]
    assert result == expected_result
    assert redis_client.called
    assert not query.called


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserEnumsRepository, "_query")
@patch.object(UserEnumsRepository, "_get_client")
async def test__query_with_cache_when_there_is_no_cache(redis_client, query, error):
    query_cache_result = None
    query_result = [["city", "city_code"]]
    redis_client_mock = AsyncMock()
    redis_client_mock.get.return_value = query_cache_result
    redis_client.return_value = redis_client_mock
    query.return_value = query_result
    result = await UserEnumsRepository._query_with_cache(sql="SQL", values={"id": 10})
    expected_result = [["city", "city_code"]]
    assert result == expected_result
    assert redis_client.called
    assert query.called


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserEnumsRepository, "_query")
@patch.object(UserEnumsRepository, "_get_client")
async def test__query_with_cache_exceptions(redis_client, query, error):
    redis_client.side_effect = Exception()
    with pytest.raises(FailedToGetData):
        result = await UserEnumsRepository._query_with_cache(
            sql="SQL", values={"id": 10}
        )
    assert error.called


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserEnumsRepository, "get_connection")
async def test__query(connection, error):
    cursor_mock = AsyncMock()
    cursor_mock.fetchall.return_value = "result"

    class ConnectionFake:
        async def __aenter__(self):
            return cursor_mock

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    connection.return_value = ConnectionFake()
    result = await UserEnumsRepository._query("SQL", values={"id": 10})
    assert result == "result"


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(UserEnumsRepository, "get_connection")
async def test__query_exception(connection, error):
    connection.side_effect = Exception()
    with pytest.raises(FailedToGetData):
        result = await UserEnumsRepository._query("SQL", values={"id": 10})
    assert error.called


