import asyncio
from src.rest.client.account import AccountRoutes
from decouple import config
import pandas as pd


base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_venues():
    # Public Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get contracts
    response = await client.venues()
    data = response['data']
    return data


if __name__ == '__main__':
    venues = asyncio.run(get_venues())
    venues_df = pd.DataFrame(venues)
    print(venues)
