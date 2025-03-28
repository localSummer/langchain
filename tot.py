import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model=os.environ.get("OPEN_API_MODEL"),
    api_key=os.environ.get("OPEN_API_KEY"),
    base_url=os.environ.get("OPEN_API_BASE"),
)

example = """
    例子：对于一个复杂的函数，添加详细描述其功能、参数和返回值的注释。
    ```javascript
    /**
     * 处理用户数据并返回结果
     * @param {Object} userData - 用户数据对象
     * @returns 处理后的用户数据
     */
    function processUserData(userData) {
      // ...代码实现...
    }
    ```
"""

system_tot_template = """
    模拟三位才华横溢、逻辑严谨的前端专家共同为代码添加注释，三位专家分别是 资深React开发专家、资深TypeScript开发专家、资深JSDoc注释专家。
    每位专家都实时详细地解释自己添加注释的思考过程，同时考虑他人之前的解释，并公开承认错误。
    在每一步，只要有可能，每位专家都会完善并基于他人的想法进行拓展，认可他们的贡献。
    他们会持续进行，直到得出问题的明确答案。
"""

system_template = """
    你是码注释专家, 你的目标是帮助用户为前端代码添加详细注释，以辅助初学者理解代码逻辑，同时保持代码的可读性和专业性。
    要求：必须使用JSDoc标准格式进行注释，不添加类型说明，优化现有注释，避免重复注释，注释位置需在代码上方，使用中文作为注释语言，注释后的代码需放入代码块中。
    输出：
        1. 注释后的代码块，不包含其他文本或Markdown语法。
        2. 输出三位专家的思考以及注释添加的过程。
    工作流：
        1. 阅读并理解提供的代码段。
        2. 根据JSDoc标准，为代码添加适当的注释。
        3. 优化现有注释，去除不必要的类型说明和重复内容。
        4. 确保注释位于代码上方，并使用中文。
        5. 将注释后的代码放入代码块中，以便复制使用。
    {data}
"""

human_tempalte = "需要添加注释的代码是：{code}"

system_tot_prompt = SystemMessagePromptTemplate.from_template(system_tot_template)
system_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_prompt = HumanMessagePromptTemplate.from_template(human_tempalte)

chat_prompt = ChatPromptTemplate(messages=[system_tot_prompt, system_prompt, human_prompt])

human_input="""
    export const useUserhBaseInfo = () => {
        const [userhBaseInfo, setIUserhBaseInfo] = useState<IUserhBaseInfo>();
        
        useEffect(() => {
            fetUserhPrivilege();
        }, []);
        
        const fetUserhPrivilege = async () => {
            const { flag, data } = await getUserhBaseInfo();
            if (flag === 1) {
                setIUserhBaseInfo(data);
            }
        };
        
        return [userhBaseInfo];
    };
"""

chain = chat_prompt | llm

result = chain.invoke({"data": example, "code": human_input})

print(result.content)

