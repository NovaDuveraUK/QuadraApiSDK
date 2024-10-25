import asyncio
from decouple import config
from src.ws.client.wsClient import WsClient

base_url = config('WS_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
company_exchange_id = config('COMPANY_EXCHANGE_ID')


async def amend_order():
    # Request amend order payload
    payload = {
      "id": "a1b2c3d4",
      "op": "trade.amend_order",
      "company_exchange_id": company_exchange_id,
      "exchange_id": "binance_spot",
      "data": {
        "order_id": "6633425015",
        "new_market_quadra": "XRP_USDT_SPOT",
        "new_order_type": "limit",
        "new_side": "sell",
        "new_base_notional": 30,
        # "new_quote_notional": 100,
        "new_price": 0.9,
        "new_time_in_force": "GTC",
        # "client_order_id": "client_order_id_1234",
        # "reduce_only": false,
        # "isolated": false,
        # "position_mode": "ONE_WAY",
        # "trigger_price": 0,
        # "trigger_type": "index_price"
      }
    }

    ws_client = WsClient(base_url, api_key, secret_key, payload)
    await ws_client.connect()


if __name__ == '__main__':
    asyncio.run(amend_order())
