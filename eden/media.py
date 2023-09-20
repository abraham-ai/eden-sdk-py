import asyncio
import httpx
from aiofiles import open as aio_open
import eden


async def upload(file_path):
    async with aio_open(file_path, 'rb') as f:
        media = await f.read()
    
    headers = {
        "x-api-key": eden.api_key,
        "x-api-secret": eden.api_secret
    }
    
    files = {'media': ('media', media)}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{eden.api_url}/media/upload",
            headers=headers,
            files=files
        )
    
    return response.json()