# llm.py功能：写一个函数，接收问题，返回DeepSeek的回答 

# import需要的库
from openai import AsyncOpenAI
import httpx
import asyncio
from config import DEEPSEEK_API_KEY # 从config.py取API密钥 

# 定义async函数，接收prompt参数 
async def ask(prompt):
    # 创建AsyncOpenAI客户端
    # client的作用是配置好下面的设置后以后只管发消息，不然每次调用都要重复一次这些设置 
    client=AsyncOpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
        http_client=httpx.AsyncClient(proxy="https://127.0.0.1:7890")
    )
    # 发请求
    response=await client.chat.completions.create(
        model=,
        messages=[{"role":,"content":}]
    )

    # 返回回答文字 
    return response.choices[0].message.

