class Transaction:
    def __init__(self, conn):
        self._conn = conn

    async def __aenter__(self):
        await self._conn.execute('BEGIN')
        return self._conn

    async def commit(self):
        await self._conn.execute('COMMIT')

    async def rollback(self):
        await self._conn.execute('ROLLBACK')

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
