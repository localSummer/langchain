from llm import llm
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# 不加下面两行会报错
class BaseCache:
    pass
class Callbacks:
    pass

db = SQLDatabase.from_uri("sqlite:///FlowerShop.db")

SQLDatabaseChain.model_rebuild()
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


response = db_chain.invoke("有多少种不同的鲜花？")
print(response)

response = db_chain.invoke("哪种鲜花的存货数量最少？")
print(response)

response = db_chain.invoke("平均销售价格是多少？")
print(response)

response = db_chain.invoke("从法国进口的鲜花有多少种？")
print(response)

response = db_chain.invoke("哪种鲜花的销售量最高？")
print(response)