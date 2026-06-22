from openai import AsyncOpenAI
import httpx
import asyncio
from config import DEEPSEEK_API_KEY

# 定义async函数，接收prompt参数
async def ask(prompt):
    # 创建AsyncOpenAI客户端
    # client的作用是配置好下面的设置后以后只管发消息，不然每次调用都要重复一次这些设置
    client =AsyncOpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
        http_client=httpx.AsyncClient(
            proxy="http://127.0.0.1:7890"
        )
    )

    # 发送请求，发送请求后得到response 
    #client.chat.completions.create是发出请求
    #await是等待，告诉Python先停在这里，等DeepSeek回答完再继续，别急着跑下一行 
    #response等DeepSeek回答回来之后把结果存在这个变量里面


    response=await client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"user","content":prompt}]
    )

    # 返回DeepSeek的回答 即返回response
    return response.choices[0].message.content

# import会运行文件里所有不在函数里的代码 
# 如果llm.py里裸写了
#result=asyncio.run(ask()) 它不在任何函数里，只要bot.py写了import llm那么这个函数会立刻运行 

# bot.py会import llm，如果没有这个保护，import的瞬间就会自动调用ask()发出请求
# 加了这行，只有直接运行llm.py时才执行下面的代码，被import时不执行

if __name__=="__main__":
    result=asyncio.run(ask("列举出近十二年图灵奖和物理学奖得主名单")) 
    # asyncio.run()的含义是"真正执行这个任务，等它跑完，把结果拿回来"
    # async def定义的函数必须用asyncio.run()启动，否则不会真的执行 
    print(result)




