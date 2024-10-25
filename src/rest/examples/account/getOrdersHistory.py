import asyncio
from src.rest.client.account import AccountRoutes
from decouple import config
import time


base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
company_exchange_id = config('COMPANY_EXCHANGE_ID')
# 1 day in milliseconds
one_day = 86400000


async def get_orders_history():
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get orders params
    params = {"company_exchange_id": company_exchange_id, "start_time": time.time() * 1000 - one_day}
    response = await client.orders_history(params)
    data = response['data']
    return data


if __name__ == '__main__':
    orders_history = asyncio.run(get_orders_history())
    print(orders_history)
