from src.rest.client.apiClient import ApiClient


class AnalyticsRoutes(ApiClient):
    async def basis_screener(self, params):
        return await self.get('/api/v1/analytics/basis-screener', params)
