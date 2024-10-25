import asyncio
from typing import List

from src.rest.client.account import AccountRoutes
from decouple import config
import pandas as pd

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_balances(ids: List[str]):
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get balance params
    params = {"company_exchange_id": ids}
    response = await client.balances(params)
    data = response['data']
    return data


if __name__ == '__main__':
    company_exchange_ids = config('COMPANY_EXCHANGE_ID')
    balances = asyncio.run(get_balances(company_exchange_ids))
    df = pd.DataFrame(balances)
    print(balances)