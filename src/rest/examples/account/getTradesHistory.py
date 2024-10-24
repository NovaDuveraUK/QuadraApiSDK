import asyncio
from src.rest.client.account import AccountRoutes
from decouple import config
import time
import pandas as pd


base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_trades_history(id: str, start_time: int, limit: int = 1000):
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get trades params
    params = {"company_exchange_id": id, "start_time": start_time, "limit": limit}
    response = await client.trades_history(params)
    data = response['data']
    return data


if __name__ == '__main__':
    company_exchange_id = config('COMPANY_EXCHANGE_ID')
    # 1 day in milliseconds
    one_day = 86400000 * 2
    start_time = int(time.time() * 1000 - one_day)
    trades_history = asyncio.run(get_trades_history(company_exchange_id, start_time))
    df = pd.DataFrame(trades_history)
    print(trades_history)
