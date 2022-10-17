import uuid
from asyncio import iscoroutine
from unittest import mock

import decouple
import pytest

from regis.src.domain.exceptions.infrastructure import ErrorToStartInfrastructure
from regis.src.infrastructures.oracle.infrastructure import OracleInfrastructure
from tests.src.infrastructures.oracle.stub_client import StubCxOracleAsyncPool


async def get_stub_pool(stub_cx_oracle_async_pool):
    return stub_cx_oracle_async_pool


@pytest.mark.asyncio
@mock.patch.object(decouple.Config, "__call__", return_value=0)
@mock.patch("cx_Oracle_async.create_pool")
async def test__get_client(create_pool_mongo_db_client, config):
    stub_cx_oracle_async_pool = StubCxOracleAsyncPool()
    create_pool_mongo_db_client.return_value = get_stub_pool(stub_cx_oracle_async_pool)
    client = await OracleInfrastructure._get_pool()
    assert client == stub_cx_oracle_async_pool
    OracleInfrastructure.pool = None


@pytest.mark.asyncio
@mock.patch.object(decouple.Config, "__call__", return_value=0)
@mock.patch("cx_Oracle_async.create_pool")
async def test__get_client_rise_infrastructure_error(
    create_pool_mongo_db_client, config
):
    create_pool_mongo_db_client.side_effect = Exception("test")
    with pytest.raises(ErrorToStartInfrastructure):
        await OracleInfrastructure._get_pool()
    OracleInfrastructure.pool = None


@pytest.mark.asyncio
@mock.patch.object(decouple.Config, "__call__", return_value=0)
@mock.patch("cx_Oracle_async.create_pool")
async def test_get_connection(create_pool_mongo_db_client, config):
    stub_cx_oracle_async_pool = StubCxOracleAsyncPool()
    create_pool_mongo_db_client.return_value = get_stub_pool(stub_cx_oracle_async_pool)
    async with OracleInfrastructure.get_connection() as cursor:
        assert cursor.id == stub_cx_oracle_async_pool.connection._cursor.id
    OracleInfrastructure.pool = None


@pytest.mark.asyncio
@mock.patch.object(decouple.Config, "__call__", return_value=0)
@mock.patch("cx_Oracle_async.create_pool")
async def test__get_pool_already_started(create_pool_mongo_db_client, config):
    assert OracleInfrastructure.pool is None
    id = uuid.uuid4()
    OracleInfrastructure.pool = id
    stub_cx_oracle_async_pool = StubCxOracleAsyncPool()
    coroutine = get_stub_pool(stub_cx_oracle_async_pool)
    create_pool_mongo_db_client.return_value = coroutine
    pool = await OracleInfrastructure._get_pool()
    assert id == pool
    if iscoroutine(coroutine):
        await coroutine
    OracleInfrastructure.pool = None
