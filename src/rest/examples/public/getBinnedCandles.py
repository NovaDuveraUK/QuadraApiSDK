import asyncio
from src.rest.client.public import PublicRoutes
from decouple import config
import pandas as pd

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
exchange_id = 'deribit'
market_quadra = 'ETH_USD_PERP_COINM'  # Get from getContracts.py
interval = '1m'


async def get_binned_candles():
    # Public Routes Class
    client = PublicRoutes(base_url, api_key, secret_key)
    # Get candles params
    params = {"exchange_id": exchange_id, "market_quadra": market_quadra, "interval": interval}
    response = await client.binned_candles(params)
    data = response['data']
    return data


if __name__ == '__main__':
    candles = asyncio.run(get_binned_candles())
    df = pd.DataFrame(candles)
    print(candles)
