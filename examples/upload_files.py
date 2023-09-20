import os
import asyncio
import eden

import dotenv
dotenv.load_dotenv()

eden.api_key = os.environ['EDEN_API_KEY']
eden.api_secret = os.environ['EDEN_API_SECRET']

file_path = "/Users/genekogan/Abraham/Misc/abraham_logo2/portrait.jpeg"

async def main():
    result = await eden.media.upload(file_path)
    print(result)

asyncio.run(main())