from src.rest.client.apiClient import ApiClient


class PublicRoutes(ApiClient):
    async def index_prices(self, params):
        return await self.get('/api/v1/public/index_prices', params)

    async def prices(self, params):
        return await self.get('/api/v1/public/prices', params)

    async def contracts(self, params):
        return await self.get('/api/v1/public/contracts', params)

    async def venues(self):
        return await self.get('/api/v1/public/venues')

    async def candles(self, params):
        return await self.get('/api/v1/public/candles-history', params)

    async def server_time(self):
        return await self.get('/api/v1/public/server-time')
