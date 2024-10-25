import asyncio
from typing import List
import json
from src.rest.client.account import AccountRoutes
from decouple import config
import pandas as pd


base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_positions(ids: List[str]):
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get position params
    params = {"company_exchange_id": ids}
    response = await client.positions(params)
    data = response['data']
    print("Positions data", data)
    return data


if __name__ == '__main__':
    company_exchange_ids = config('COMPANY_EXCHANGE_ID')
    positions = asyncio.run(get_positions(company_exchange_ids))
    df = pd.DataFrame(positions)
    print(positions)