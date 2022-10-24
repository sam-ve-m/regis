import uuid
from unittest import mock

import pytest
import decouple

from regis.src.domain.exceptions.infrastructure import (
    ErrorToStartInfrastructure,
)
from regis.src.infrastructures.redis import RedisInfrastructure
from tests.src.infrastructures.redis.stub_client import StubAsyncRedis





@pytest.mark.asyncio
@mock.patch("aioredis.from_url")
@mock.patch.object(decouple.Config, "__call__", return_value="redis://teste")
async def test__get_client(get_redis_url, new_redis_client):
    stub_redis_client = StubAsyncRedis()
    new_redis_client.return_value = stub_redis_client
    client = RedisInfrastructure._get_client()
    assert client == stub_redis_client
    RedisInfrastructure.redis = None


@pytest.mark.asyncio
@mock.patch("aioredis.from_url")
@mock.patch.object(decouple.Config, "__call__", return_value="redis://teste")
async def test__get_client_rise_infrastructure_error(get_redis_url, new_redis_client):
    new_redis_client.side_effect = Exception("test")
    with pytest.raises(ErrorToStartInfrastructure):
        RedisInfrastructure._get_client()
    RedisInfrastructure.redis = None


@pytest.mark.asyncio
@mock.patch("aioredis.from_url")
@mock.patch.object(decouple.Config, "__call__", return_value="redis://teste")
async def test__get_client_already_started(get_redis_url, new_redis_client):
    assert RedisInfrastructure.redis is None
    id = uuid.uuid4()
    RedisInfrastructure.redis = id
    stub_redis_client = StubAsyncRedis()
    new_redis_client.return_value = stub_redis_client
    assert id == RedisInfrastructure._get_client()
    RedisInfrastructure.redis = None
