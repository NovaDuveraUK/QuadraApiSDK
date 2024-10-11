import asyncio
from decouple import config
from src.ws.client.wsClient import WsClient

base_url = config('WS_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
company_exchange_id = config('COMPANY_EXCHANGE_ID')


async def cancel_order():
    # Request cancel order payload
    payload = {
      "id": "a1b2c3d4",
      "op": "trade.cancel_order",
      "company_exchange_id": company_exchange_id,
      "exchange_id": "binance_spot",
      "data": {
        "market_quadra": "XRP_USDT_SPOT",
<<<<<<< HEAD
        "order_id": "6637358689"
=======
        "order_id": "6634198389"
>>>>>>> 34970be815b0865a82da9c3712c9800515e4b9df
      }
    }

    ws_client = WsClient(base_url, api_key, secret_key, payload)
    await ws_client.connect()


if __name__ == '__main__':
    asyncio.run(cancel_order())