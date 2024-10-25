import asyncio
from decouple import config
from src.ws.client.wsClient import WsClient

base_url = config('WS_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
company_exchange_id = config('COMPANY_EXCHANGE_ID')


async def listen_algo_orders():
    # Listen algo orders payload
    payload = {
        'op': 'subscribe',
        'topic_id': 'algo_orders',
        'params': {
            'company_exchange_id': company_exchange_id
        }
    }

    ws_client = WsClient(base_url, api_key, secret_key, payload)
    await ws_client.connect()


if __name__ == '__main__':
    asyncio.run(listen_algo_orders())
