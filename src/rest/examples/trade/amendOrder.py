import asyncio
from src.rest.client.trade import TradeRoutes
from decouple import config

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')

# Note symbol will be changing to 'market_quadra' in the future

example_order = {
    "company_exchange_id": "",
    "exchange_id": "binance_spot",
    "exchange_format": 0,
    "data": {
        "order_id": "xxx",
        "new_market_quadra": "XRP_USDT_SPOT",
        "new_order_type": "limit",
        "new_side": "buy",
        "new_base_notional": 40,
        "new_price": 0.42,
        "new_time_in_force": "GTC",
        "new_post_only": True
    }
}


async def amend_order():
    # Trade Routes Class
    client = TradeRoutes(base_url, api_key, secret_key)
    response = await client.amend_order(example_order)
    data = response['data']
    return data


if __name__ == '__main__':
    order = asyncio.run(amend_order())
    print(order)
