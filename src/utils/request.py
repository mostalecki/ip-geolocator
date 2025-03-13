import httpx


async def send_request(*args, **kwargs):
    async with httpx.AsyncClient() as client:
        return await client.get(*args, **kwargs)
