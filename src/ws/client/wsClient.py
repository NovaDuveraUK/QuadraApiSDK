import asyncio
import websockets
import hmac
import hashlib
import time
import json
from urllib.parse import urlencode
from decouple import config

base_url = config('WS_API_URL_LOCAL')
api_key = config('API_KEY')
secret_key = config('SECRET_KEY')


class WsClient:
    def __init__(self, base_url, api_key, secret_key, query=None):
        self.query = query
        self.base_url = base_url
        self.api_key = api_key
        self.secret_key = secret_key
        self.connection = None

    async def connect(self):
        try:
            print("Attempting to connect...")
            self.connection = await websockets.connect(self.base_url)
            await self.on_open()
            await self.listen()  # Start listening for messages
        except Exception as e:
            await self.on_error(e)

    async def listen(self):
        try:
            async for message in self.connection:
                await self.on_message(message)
        except websockets.ConnectionClosed as e:
            await self.on_close(e)

    async def send(self, message):
        print("Sending message: ", message)
        if self.connection:
            print("Conn:")
            await self.connection.send(message)

    async def close(self):
        if self.connection:
            await self.connection.close()
            await self.on_close(None)

    # Event Handlers (to be customized)
    async def on_open(self):
        print(f"Connection established to {self.base_url}")

        print("Attempting to login...")
        login = self.login()
        await self.send(login)
        print("Running query")
        if self.query:
            await self.send(json.dumps(self.query))

    async def on_message(self, message):
        print(f"Received message: {message}")

    async def on_error(self, error):
        print(f"Error: {error}")

    async def on_close(self, error):
        if error:
            print(f"Connection closed with error: {error}")
        else:
            print("Connection closed normally.")

    def _generate_signature(self, method, endpoint):
        timestamp = str(int(time.time() * 1000))
        request_path = endpoint

        message = f"{timestamp}{method}{request_path}"
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

        return timestamp, signature

    def login(self, method='GET', endpoint='/ws/login'):
        timestamp, signature = self._generate_signature(method, endpoint)

        login = {
            'op': 'login',
            'api-key': self.api_key,
            'signature': signature,
            'timestamp': timestamp
        }

        return json.dumps(login)


# Example usage
async def main():
    ws_client = WsClient(base_url, api_key, secret_key)
    await ws_client.connect()


# Run the WebSocket client
if __name__ == "__main__":
    asyncio.run(main())
