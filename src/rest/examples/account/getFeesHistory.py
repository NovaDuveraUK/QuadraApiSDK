import asyncio
from src.rest.client.account import AccountRoutes
from decouple import config
import time
import pandas as pd

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
company_exchange_id = config('COMPANY_EXCHANGE_ID')
# 1 day in milliseconds
one_day = 86400000 * 7

FEE_TYPE = 'funding_fee'


async def get_fees_history():
    # Account Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get fees params
    params = {"company_exchange_id": company_exchange_id, "fee_type": FEE_TYPE, "start_time": time.time() * 1000 - one_day}
    response = await client.fees_history(params)
    data = response['data']
    return data


if __name__ == '__main__':
    fees_history = asyncio.run(get_fees_history())
    df = pd.DataFrame(fees_history)
    print(fees_history)
