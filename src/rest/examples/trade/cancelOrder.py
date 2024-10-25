import asyncio
from src.rest.client.trade import TradeRoutes
from decouple import config

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')

example_order = {
  "company_exchange_id": "",
  "exchange_id": "binance_usdm",
  "exchange_format": 0,
  "data": {
    "market_quadra": "XRP_USDT_PERP_USDM",
    "order_id": "xxx",
  }
}


async def cancel_order():
    # Trade Routes Class
    client = TradeRoutes(base_url, api_key, secret_key)
    response = await client.cancel_order(example_order)
    data = response['data']
    return data


if __name__ == '__main__':
    order = asyncio.run(cancel_order())
    print(order)
