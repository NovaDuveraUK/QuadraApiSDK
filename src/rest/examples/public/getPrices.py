import asyncio
from src.rest.client.public import PublicRoutes
from decouple import config
import pandas as pd

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_price():
    # Public Routes Class
    client = PublicRoutes(base_url, api_key, secret_key)
    # Get prices params
    params = {"exchange_id": exchange_id, "market_quadra": market_quadra}
    response = await client.prices(params)
    data = response['data']
    return data


async def get_price_by_symbol(exchange_id: str, symbol: str):
    # Public Routes Class
    client = PublicRoutes(base_url, api_key, secret_key)
    # Get prices params
    params = {"exchange_id": exchange_id, "symbol": symbol}
    response = await client.prices(params)
    data = response['data']
    return data


if __name__ == '__main__':
    exchange_id = 'binance_spot'
    market_quadra = 'BTC_USDT_SPOT'  # Get from getContracts.py
    price = asyncio.run(get_price())
    price_df = pd.DataFrame(price)
    print(price)
