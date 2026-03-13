import asyncio
import time
import os
from concurrent.futures import ProcessPoolExecutor

def check_stock(item):
    print(f"Checking {item} in store...")
    time.sleep(3) #blocking operation
    print(os.getpid()) 
    return f"{item} stock:42"


async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool,check_stock,"Tea")
        print(result)
      
        
if __name__ == "__main__":
    print("main of ",{os.getpid()})
    asyncio.run(main())
print(f"H of process of pid : {os.getpid()}")
