import asyncio

async def say_hello():
    print("开始等待...")
    await asyncio.sleep(2)
    print("等待结束，你好！")

asyncio.run(say_hello())