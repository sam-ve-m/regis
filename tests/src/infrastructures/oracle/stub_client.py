from contextlib import asynccontextmanager
import uuid


class StubCxOracleAsyncPool:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.connection = StubCxOracleAsyncConnection()

    @asynccontextmanager
    async def acquire(self):
        yield self.connection


class StubCxOracleAsyncConnection:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._cursor = StubCxOracleAsyncCursor()

    @asynccontextmanager
    async def cursor(self):
        yield self._cursor

    async def commit(self):
        pass


class StubCxOracleAsyncCursor:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.id = uuid.uuid4()
