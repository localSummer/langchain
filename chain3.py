from re import VERBOSE, template


flower_care_template = """你是一个经验丰富的园丁，擅长解答关于养花育花的问题。
                        下面是需要你来回答的问题:
                        {input}"""

flower_deco_template = """你是一位网红插花大师，擅长解答关于鲜花装饰的问题。
                        下面是需要你来回答的问题:
                        {input}"""
    
# 构建list结构便于后续程序使用                    
prompt_infos = [
    {
        "key": "flower_care",
        "description": "适合回答关于鲜花护理的问题",
        "template": flower_care_template
    },
    {
        "key": "flower_deco",
        "description": "适合回答关于鲜花装饰的问题",
        "template": flower_deco_template
    }
]

from llm import llm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

chain_map = {}

for info in prompt_infos:
    prompt = PromptTemplate(template=info['template'], input_variables=['input'])
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    chain_map[info['key']] = chain
    
    
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE as RouterTemplate

destinations = [f"{p['key']}: {p['description']}" for p in prompt_infos]

router_template = RouterTemplate.format(destinations="\n".join(destinations))
# print("路由模板:\n",router_template)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser()
)

router_chain = LLMRouterChain.from_llm(llm, router_prompt, verbose=True)

from langchain.chains.conversation.base import ConversationChain

default_chain = ConversationChain(llm=llm, output_key="text", verbose=True)

from langchain.chains.router import MultiPromptChain

chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=chain_map,
    default_chain=default_chain,
    verbose=True
)

result = chain.invoke({
    "input": "如何考入哈佛大学？"
})

print(result)