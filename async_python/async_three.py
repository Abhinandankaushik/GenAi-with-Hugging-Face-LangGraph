import asyncio
import aiohttp

async def fetch_url(session,url):
    async with session.get(url) as response:
        print(f"Fetched {url} with status {response.status}")
        

async def main():
    urls = ["https://httpbin.org/delay/2"]*3
    async with aiohttp.ClientSession() as session:
        task = [fetch_url(session,url) for url in urls]
        print(task)
        await asyncio.gather(*task)
        
   
asyncio.run(main())        