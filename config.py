from dotenv import load_dotenv
import os

load_dotenv()

DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
QDRANT_URL=os.getenv("QDRANT_URL")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")

if DEEPSEEK_API_KEY == None:
    raise ValueError("缺少DEEPSEEK_API_KEY，请检查.env文件")
elif TELEGRAM_BOT_TOKEN == None:
    raise ValueError("缺少TELEGRAM_BOT_TOKEN，请检查文件")
elif QDRANT_URL == None:
    raise ValueError("缺少QDRANT_URL，请检查文件")
elif QDRANT_API_KEY == None:
    raise ValueError("缺少QDRANT_API_KEY，请检查文件")
elif TAVILY_API_KEY == None:
    raise ValueError("缺少TAVILY_API_KEY，请检查文件")
