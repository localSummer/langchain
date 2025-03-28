from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    api_key=os.environ.get('OPEN_API_KEY'),
    model=os.environ.get('OPEN_API_MODEL'),
    base_url=os.environ.get('OPEN_API_BASE'),
    verbose=True
)

llm_embedding = OpenAIEmbeddings(model=os.environ.get('ONE_API_MODEL'), api_key=os.environ.get('ONE_API_KEY'), base_url=os.environ.get('ONE_API_BASE'))

def get_llm(**kwargs):
    # 从 kwargs 中获取 temperature 参数，如果不存在则使用默认值 0，并将其传递给 ChatOpenAI 初始化函数
    temperature = kwargs.get('temperature', 0)
    # 从 kwargs 移除 temperature 参数，避免传递给 ChatOpenAI 初始化函数
    kwargs.pop('temperature', None)
    # 初始化 ChatOpenAI 实例，将 temperature 参数设置为传递给函数的 temperature 参数值，其他参数使用 **kwargs 传递
    try:
        llm = ChatOpenAI(
            temperature=temperature,
            api_key=os.environ.get('OPEN_API_KEY'),
            model=os.environ.get('OPEN_API_MODEL'),
            base_url=os.environ.get('OPEN_API_BASE'),
            verbose=True,
            **kwargs
        )
        return llm
    except Exception as e:
        print(f'Error initializing ChatOpenAI: {e}')
        return None
