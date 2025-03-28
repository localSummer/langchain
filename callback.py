import asyncio
from typing import Any, Dict, List
from langchain.schema import LLMResult, HumanMessage
from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler
from llm import get_llm

class MyFlowerShopSyncHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"获取花卉数据: token: {token}")
        
class MyFlowerShopAsyncHandler(AsyncCallbackHandler):
    async def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        print("正在获取花卉数据...")
        await asyncio.sleep(1)
        print("花卉数据获取完毕。提供建议...")

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        print("整理花卉建议...")
        await asyncio.sleep(0.5)
        print("祝你今天愉快！")

async def main():
    flower_shop_chat = get_llm(max_tokens=100, streaming=True, callbacks=[MyFlowerShopSyncHandler(), MyFlowerShopAsyncHandler()])
    await flower_shop_chat.agenerate([[HumanMessage(content="哪种花卉最适合生日？只简单说3种，不超过50字")]])
       
asyncio.run(main())  
    