class StubAsyncRedis:
    def __init__(self, values: dict = None, *args, **kwargs):
        if values is None:
            values = dict()
        self.args = args
        self.kwargs = kwargs
        self.values = values

    async def get(self, key):
        return self.values.get(key)

    async def set(self, key, value):
        self.values.update({key: value})
