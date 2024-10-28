import asyncio
from src.rest.client.account import AccountRoutes
from decouple import config
import time
import pandas as pd

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_balances_history(id: str, start_time: int):
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get balances params
    params = {"company_exchange_id": id, "start_time": start_time}
    response = await client.balances_history(params)
    data = response['data']
    return data


if __name__ == '__main__':
    # 1 day in milliseconds
    one_day = 86400000
    company_exchange_id = config('COMPANY_EXCHANGE_ID')
    start = int(time.time() * 1000 - one_day)
    balances_history = asyncio.run(get_balances_history(company_exchange_id, start))
    df = pd.DataFrame(balances_history)
    print(balances_history)