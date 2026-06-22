from openai import AsyncOpenAI
import httpx
from config import DEEPSEEK_API_KEY

async def ask(prompt):
    client =AsyncOpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
        # 忘记格式了，不知道格式怎么写 https://127.0.0.1:7890
    )

    # 接收提问
    response=


    # 返回DeepSeek的回答 
    response=


