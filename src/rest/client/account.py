from src.rest.client.apiClient import ApiClient


class AccountRoutes(ApiClient):
    async def balances(self, params):
        return await self.get('/api/v1/account/balances', params)

    async def positions(self, params):
        return await self.get('/api/v1/account/positions', params)

    async def open_orders(self, params):
        return await self.get('/api/v1/account/open-orders', params)

    async def venues(self):
        return await self.get('/api/v1/account/venues')

    async def balances_history(self, params):
        return await self.get('/api/v1/account/balances-history', params)

    async def positions_history(self, params):
        return await self.get('/api/v1/account/positions-history', params)

    async def orders_history(self, params):
        return await self.get('/api/v1/account/orders-history', params)

    async def trades_history(self, params):
        return await self.get('/api/v1/account/trades-history', params)

    async def fees_history(self, params):
        return await self.get('/api/v1/account/fees-history', params)

    async def transfers_history(self, params):
        return await self.get('/api/v1/account/transfers-history', params)
