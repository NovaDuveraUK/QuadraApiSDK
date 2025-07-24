import asyncio

from src.rest.client.analytics import AnalyticsRoutes
from decouple import config
import pandas as pd

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_basis_screener(
        base_exchange: str = None,
        quote_exchange: str = None,
        base_inst_type: str = None,
        quote_inst_type: str = None,
        base_risk_type: str = None,
        quote_risk_type: str = None,
        base: str = None,
    ):
    # Analytics Routes Class
    client = AnalyticsRoutes(base_url, api_key, secret_key)

    params = {}

    if base_exchange is not None:
        params['base_exchange'] = base_exchange

    if quote_exchange is not None:
        params['quote_exchange'] = quote_exchange

    if base_inst_type is not None:
        params['base_inst_type'] = base_inst_type

    if quote_inst_type is not None:
        params['quote_inst_type'] = quote_inst_type

    if base_risk_type is not None:
        params['base_risk_type'] = base_risk_type

    if quote_risk_type is not None:
        params['quote_risk_type'] = quote_risk_type

    if base is not None:
        params['base'] = base

    # Get Basis Screener

    response = await client.basis_screener(params)
    data = response['data']
    return data


if __name__ == '__main__':
    basis_screener = asyncio.run(get_basis_screener(base_inst_type='perp', base_risk_type='inverse'))
    df = pd.DataFrame(basis_screener)
    print(basis_screener)
