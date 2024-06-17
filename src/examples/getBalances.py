import asyncio
from src.quadra.account import AccountRoutes
from decouple import config


base_url = 'http://localhost:3000'
# base_url = 'https://dev-execution-api.quadra.trade'
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')
exchange = 'binance_spot'
company_exchange_id = 'ed47cf96-2ba8-49b9-9f2a-e0d67e6c428e'


async def get_balances():
    # Public Routes Class
    client = AccountRoutes(base_url, api_key, secret_key)
    # Get contracts
    params = {"exchange": exchange, "company_exchange_id": company_exchange_id}
    contracts_response = await client.balances(params)
    print(contracts_response)
    contracts_data = contracts_response['data']
    return contracts_data


# Example main gutter script below
if __name__ == '__main__':
    contracts = asyncio.run(get_balances())