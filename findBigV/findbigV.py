import re

from langchain.prompts import PromptTemplate
from agents.weibo_agent import lookup_V
from tools.general_tool import remove_non_chinese_fields
from tools.scraping_tool import get_data
from llm import get_llm
from langchain.chains.llm import LLMChain
from tools.textgen_tool import generate_letter

def find_bigV(flower: str):
    # response_UID = lookup_V(flower_type="牡丹")
    # print(response_UID)
    
    # UID = re.findall(r'\d+', response_UID)[0]
    # print("这位鲜花大V的微博ID是", UID)
    
    person_info = get_data('7800874740')
    person_info = remove_non_chinese_fields(person_info)
    # print(person_info)
    
    result = generate_letter(person_info)
    # print(result)
    return result
