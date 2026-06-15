from unittest import result
from openai import AsyncOpenAI
from config import DEEPSEEK_API_KEY
import asyncio
import httpx



async def ask(prompt):
    client = AsyncOpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
        http_client=httpx.AsyncClient(
            proxy="http://127.0.0.1:7890"
    )
)

    response=await client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"user","content":prompt}]   
    )

    return response.choices[0].message.content

## resulu = ask("你好")
## print(result)
## 如果这两句写在函数外面，会出现问题。import一个文件时会执行不在函数里的代码，所以import llm时会自动运行ask
## 如果采用以下固定写法，则不会出现该问题

if __name__ == "__main__":
    result = asyncio.run(ask("给我列举近10年图灵奖得主国籍与名单"))
    print(result)

