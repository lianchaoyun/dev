import solana
from solana.rpc.api import Client
import asyncio
from solana.rpc.async_api import AsyncClient

http_client = Client("https://api.devnet.solana.com")

async def main():
    #async with AsyncClient("https://api.devnet.solana.com") as client:
    #    res = await client.is_connected()
    #print(res)  # True

    # Alternatively, close the client explicitly instead of using a context manager:
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()
    print(res)  # True
    await client.close()

asyncio.run(main())