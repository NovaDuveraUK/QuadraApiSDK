import asyncio
from src.rest.client.public import PublicRoutes
from decouple import config

base_url = config('REST_API_URL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


async def get_server_time():
    # Public Routes Class
    client = PublicRoutes(base_url, api_key, secret_key)
    response = await client.server_time()
    data = response['data']
    return data


if __name__ == '__main__':
    server_time = asyncio.run(get_server_time())
    print(server_time)
