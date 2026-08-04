from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langchain_openai import ChatOpenAI


# 状态
class AgentState(TypedDict):

    query: str

    sql: str

    result: str

    analysis: str

    report: str

    validation: dict

    insight: dict


# 初始化模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-15666e1260e0496f80c8dbd544ae0d39",
    base_url="https://api.deepseek.com"
)


# LLM节点
def analyst_node(state):

    question = state["question"]

    response = llm.invoke(
        f"""
你是一名商业数据分析师。

请分析：

{question}

要求：
给出原因分析和建议。
"""
    )


    return {
        "answer": response.content
    }



graph_builder = StateGraph(AgentState)


graph_builder.add_node(
    "analyst",
    analyst_node
)


graph_builder.add_edge(
    START,
    "analyst"
)


graph_builder.add_edge(
    "analyst",
    END
)


graph = graph_builder.compile()


result = graph.invoke(
    {
        "question":
        "分析今年销售下降原因",
        "answer":""
    }
)


print(result["answer"])