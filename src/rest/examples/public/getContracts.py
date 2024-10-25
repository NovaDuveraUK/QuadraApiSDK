import asyncio
from src.rest.client.public import PublicRoutes
from decouple import config

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
exchange_id = 'binance_spot'


async def get_contracts():
    # Public Routes Class
    client = PublicRoutes(base_url, api_key, secret_key)
    # Get contracts params
    params = {"exchange_id": exchange_id}
    response = await client.contracts(params)
    data = response['data']
    return data


if __name__ == '__main__':
    contracts = asyncio.run(get_contracts())
    print(contracts[0])
