import asyncio
from src.rest.client.trade import TradeRoutes
from decouple import config

base_url = config('REST_API_URL_LOCAL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')

# Note symbol will be changing to 'market_quadra' in the future

example_order = {
  "company_exchange_id": "",
  "exchange_id": "binance_coinm",
  "exchange_format": 0,
  "data": {
    "market_quadra": "DOT_USD_PERP_COINM",
    "order_type": "limit",
    "side": "buy",
    "quote_notional": 20,
    "price": 0.2,
    "time_in_force": "GTC",
    "post_only": True
  }
}


async def place_order():
    # Trade Routes Class
    client = TradeRoutes(base_url, api_key, secret_key)
    response = await client.place_order(example_order)
    data = response['data']
    return data


if __name__ == '__main__':
    order = asyncio.run(place_order())
    print(order)
