from loguru import logger
from langchain.callbacks import FileCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_openai.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

logfile = 'log.txt'
logger.add(logfile, colorize=True, enqueue=True, rotation="100 MB", retention="10 days")

handler = FileCallbackHandler(logfile)

prompt = PromptTemplate.from_template("1 + {number} = ")
llm = ChatOpenAI(
    temperature=0,
    model=os.environ.get("OPEN_API_MODEL"),
    api_key=os.environ.get("OPEN_API_KEY"),
    base_url=os.environ.get("OPEN_API_BASE"),
    callbacks=[handler],
    verbose=True
)

chain = prompt | llm

result = chain.invoke({"number": 2})
print(result.content)


