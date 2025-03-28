from langchain.prompts import FewShotPromptTemplate, PromptTemplate, SemanticSimilarityExampleSelector
from langchain_openai.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()

samples = [
  {
  "flower_type": "玫瑰",
  "occasion": "爱情",
  "ad_copy": "玫瑰，浪漫的象征，是你向心爱的人表达爱意的最佳选择。"
  },
  {
  "flower_type": "康乃馨",
  "occasion": "母亲节",
  "ad_copy": "康乃馨代表着母爱的纯洁与伟大，是母亲节赠送给母亲的完美礼物。"
  },
  {
  "flower_type": "百合",
  "occasion": "庆祝",
  "ad_copy": "百合象征着纯洁与高雅，是你庆祝特殊时刻的理想选择。"
  },
  {
  "flower_type": "向日葵",
  "occasion": "鼓励",
  "ad_copy": "向日葵象征着坚韧和乐观，是你鼓励亲朋好友的最好方式。"
  }
]

template = "鲜花类型: {flower_type}\n场合: {occasion}\n文案: {ad_copy}"
prompt_sample = PromptTemplate.from_template(template)

example_selectors = SemanticSimilarityExampleSelector.from_examples(
  samples,
  OpenAIEmbeddings(model=os.environ.get('ONE_API_MODEL'), api_key=os.environ.get('ONE_API_KEY'), base_url=os.environ.get('ONE_API_BASE')),
  Chroma,
  k = 1
)

prompt = FewShotPromptTemplate(example_selector = example_selectors, example_prompt = prompt_sample, suffix = "鲜花类型: {flower_type}\n场合: {occasion} ", input_variables = ["flower_type", "occasion"])

chat_model = ChatOpenAI(model=os.environ.get('OPEN_API_MODEL'), openai_api_key=os.environ.get('OPEN_API_KEY'), openai_api_base=os.environ.get('OPEN_API_BASE'))

chain = prompt | chat_model

result = chain.invoke({"flower_type": "康乃馨", "occasion": "母亲节"})

print(result.content)
