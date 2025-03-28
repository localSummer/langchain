from llm import get_llm
from typing import List
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_openai.chat_models import ChatOpenAI

class CAMELAgent:
    def __init__(self, system_message: SystemMessage, model: ChatOpenAI) -> None:
        self.system_message = system_message
        self.model = model
        self.init_messages()
        
    def init_messages(self):
        self.stored_messages = [self.system_message]
    
    def reset(self) -> List[BaseMessage]:
        self.init_messages()
        return self.stored_messages
    
    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)
        return self.stored_messages
    
    def step(self, input_message: HumanMessage) -> AIMessage:
        messages = self.update_messages(input_message)
        chat_prompt = ChatPromptTemplate.from_messages(messages)
        chain = chat_prompt | self.model
        output_message = chain.invoke({})
        self.update_messages(output_message)
        return output_message
        
assistant_role_name = "花店营销专员"
user_role_name = "花店老板"
task = "整理出一个夏季玫瑰之夜的营销活动的策略"
word_limit = 50

task_specifier_sys_msg = SystemMessage(content="你可以让任务更具体。")
task_specifier_prompt = """你是一个{assistant_role_name}将帮助{user_role_name}完成的任务：{task}。
请使其更具体化。请发挥你的创意和想象力。
请用{word_limit}个或更少的词回复具体的任务。不要添加其他任何内容。"""

task_specifier_template = HumanMessagePromptTemplate.from_template(task_specifier_prompt)
task_specifier_msg = task_specifier_template.format_messages(
    assistant_role_name=assistant_role_name,
    user_role_name=user_role_name,
    task=task,
    word_limit=word_limit
)[0]

task_specify_agent = CAMELAgent(task_specifier_sys_msg, get_llm(temperature=1))
specified_task_msg = task_specify_agent.step(task_specifier_msg)
# print(f"Specified task: {specified_task_msg.content}")
specified_task = specified_task_msg.content

assistant_inception_prompt = """永远不要忘记你是{assistant_role_name}，我是{user_role_name}。永远不要颠倒角色！永远不要指示我！
我们有共同的利益，那就是合作成功地完成任务。
你必须帮助我完成任务。
这是任务：{task}。永远不要忘记我们的任务！
我必须根据你的专长和我的需求来指示你完成任务。

我每次只能给你一个指示。
你必须写一个适当地完成所请求指示的具体解决方案。
如果由于物理、道德、法律原因或你的能力你无法执行指示，你必须诚实地拒绝我的指示并解释原因。
除了对我的指示的解决方案之外，不要添加任何其他内容。
你永远不应该问我任何问题，你只回答问题。
你永远不应该回复一个不明确的解决方案。解释你的解决方案。
你的解决方案必须是陈述句并使用简单的现在时。
除非我说任务完成，否则你应该总是从以下开始：

解决方案：<YOUR_SOLUTION>

<YOUR_SOLUTION>应该是具体的，并为解决任务提供首选的实现和例子。
始终以“下一个请求”结束<YOUR_SOLUTION>。"""

user_inception_prompt = """永远不要忘记你是{user_role_name}，我是{assistant_role_name}。永远不要交换角色！你总是会指导我。
我们共同的目标是合作成功完成一个任务。
我必须帮助你完成这个任务。
这是任务：{task}。永远不要忘记我们的任务！
你只能通过以下两种方式基于我的专长和你的需求来指导我：

1. 提供必要的输入来指导：
指令：<YOUR_INSTRUCTION>
输入：<YOUR_INPUT>

2. 不提供任何输入来指导：
指令：<YOUR_INSTRUCTION>
输入：无

“指令”描述了一个任务或问题。与其配对的“输入”为请求的“指令”提供了进一步的背景或信息。

你必须一次给我一个指令。
我必须写一个适当地完成请求指令的回复。
如果由于物理、道德、法律原因或我的能力而无法执行你的指令，我必须诚实地拒绝你的指令并解释原因。
你应该指导我，而不是问我问题。
现在你必须开始按照上述两种方式指导我。
除了你的指令和可选的相应输入之外，不要添加任何其他内容！
继续给我指令和必要的输入，直到你认为任务已经完成。
当任务完成时，你只需回复一个单词<CAMEL_TASK_DONE>。
除非我的回答已经解决了你的任务，否则永远不要说<CAMEL_TASK_DONE>。"""

def get_sys_msgs(assistant_role_name: str, user_role_name: str, task: str):
    assistant_sys_template = SystemMessagePromptTemplate.from_template(assistant_inception_prompt)
    assistant_sys_msg = assistant_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task
    )[0]
    
    user_sys_template = SystemMessagePromptTemplate.from_template(user_inception_prompt)
    user_sys_msg = user_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task
    )[0]
    
    return assistant_sys_msg, user_sys_msg

assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task)

assistant_agent = CAMELAgent(assistant_sys_msg, get_llm(temperature=0.2))
user_agent = CAMELAgent(user_sys_msg, get_llm(temperature=0.2))
assistant_agent.reset()
user_agent.reset()

assistant_msg = HumanMessage(
    content=(
        f"{user_sys_msg.content}。"
        "现在开始逐一给我介绍。"
        "只回复指令和输入。"
    )
)
user_msg = HumanMessage(
    content=f"{assistant_sys_msg.content}"
)

print(user_msg.content)
user_msg = assistant_agent.step(user_msg)

# print(f"Original task prompt:\n{task}\n")
# print(f"Specified task prompt:\n{specified_task}\n")

chat_turn_limit, n = 30, 0

while n < chat_turn_limit:
    n += 1
    user_ai_msg = user_agent.step(user_msg)
    user_msg = HumanMessage(content=user_ai_msg.content)
    print(f"AI User ({user_role_name}):\n\n{user_msg.content}\n\n")
    assistant_ai_msg = assistant_agent.step(user_msg)
    assistant_msg = HumanMessage(content=assistant_ai_msg.content)
    print(f"AI Assistant ({assistant_role_name}):\n\n{assistant_msg.content}\n\n")
    if "<CAMEL_TASK_DONE>" in user_msg.content:
        break