import asyncio
from typing import List

from src.rest.client.account import AccountRoutes
from decouple import config

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_open_orders(ids: List[str]):
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get open order params
    params = {"company_exchange_id": ids}
    response = await client.open_orders(params)
    data = response['data']
    return data


if __name__ == '__main__':
    company_exchange_ids = config('COMPANY_EXCHANGE_ID')
    open_orders = asyncio.run(get_open_orders(company_exchange_ids))
    print(open_orders)