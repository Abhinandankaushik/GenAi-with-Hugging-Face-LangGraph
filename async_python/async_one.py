import asyncio

async def brew_tea():
    print("Brewing tea...")
    await asyncio.sleep(2)
    print("Tea is ready")
    

asyncio.run(brew_tea())
