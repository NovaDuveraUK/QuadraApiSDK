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


async def get_transfers_history():
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get trades params
    params = {"company_exchange_id": company_exchange_id, "start_time": time.time() * 1000 - one_day}
    response = await client.transfers_history(params)
    data = response['data']
    return data


if __name__ == '__main__':
    transfers_history = asyncio.run(get_transfers_history())
    print(transfers_history)
