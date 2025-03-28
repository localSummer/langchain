import asyncio

async def compute(x, y, callback):
    print("starting compute...")
    await asyncio.sleep(0.5)
    result = x + y
    callback(result)
    print("finished compute...")

def print_result(value):
    print(f"the result is: {value}")

async def another_task():
    print("starting another task...")
    await asyncio.sleep(1)
    print("finished another task")

async def main():
    print("Main starts...")
    task1 = asyncio.create_task(compute(3, 4, print_result))
    task2 = asyncio.create_task(another_task())
    
    await task1
    await task2

asyncio.run(main())