import asyncio
import time
async def brew(name):
    print(f"Brewing {name}...")
    # await asyncio.sleep(2)  #it dosen't block the event loop
    time.sleep(2)             #it blocks event loop and current thread as well
    print(f"{name} is ready")
    
    
async def main():
    await asyncio.gather(
        brew("tea"),
        brew("coffe"),
        brew("milk")
    )
    
asyncio.run(main())

