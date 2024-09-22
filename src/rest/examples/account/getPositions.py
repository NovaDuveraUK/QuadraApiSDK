import asyncio
from src.rest.client.account import AccountRoutes
from decouple import config
import pandas as pd


base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
company_exchange_id = config('COMPANY_EXCHANGE_ID')


async def get_positions():
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get position params
    params = {"company_exchange_id": company_exchange_id}
    response = await client.positions(params)
    data = response['data']
    return data


if __name__ == '__main__':
    positions = asyncio.run(get_positions())
    df = pd.DataFrame(positions)
    print(positions)