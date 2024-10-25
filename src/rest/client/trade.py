from src.rest.client.apiClient import ApiClient


class TradeRoutes(ApiClient):
    async def place_order(self, data):
        return await self.post('/api/v1/trade/place_order', data=data)

    async def amend_order(self, data):
        return await self.post('/api/v1/trade/amend_order', data=data)

    async def check_order(self, data):
        return await self.post('/api/v1/trade/check_order', data=data)

    async def cancel_order(self, data):
        return await self.post('/api/v1/trade/cancel_order', data=data)
