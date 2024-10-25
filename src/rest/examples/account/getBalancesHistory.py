import asyncio
from src.rest.client.account import AccountRoutes
from decouple import config
import time
import pandas as pd

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
company_exchange_id = config('COMPANY_EXCHANGE_ID')
# 1 day in milliseconds
one_day = 86400000


async def get_balances_history():
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get balances params
    params = {"company_exchange_id": company_exchange_id, "start_time": time.time() * 1000 - one_day}
    response = await client.balances_history(params)
    data = response['data']
    return data


if __name__ == '__main__':
    balances_history = asyncio.run(get_balances_history())
    df = pd.DataFrame(balances_history)
    print(balances_history)