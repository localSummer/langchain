from llm import llm
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentType, initialize_agent

tools = load_tools(["serpapi", "llm-math"], llm=llm)

agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.invoke({
    "input": "目前市场上玫瑰花的平均价格是多少？如果我在此基础上加价15%卖出，应该如何定价？"
})