import os
import sys



# ==============================
# 添加项目根目录到 Python路径
# ==============================


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


if BASE_DIR not in sys.path:

    sys.path.insert(
        0,
        BASE_DIR
    )



# ==============================
# 导入Agent调用函数
# ==============================


from agents.sql_agent import run_agent




# ==============================
# 提供给 Streamlit调用
# ==============================


def run_analysis(question):


    """
    调用商业分析Agent

    参数:
        question:
            用户输入的问题

    返回:
        LangGraph执行后的state
    """


    result = run_agent(

        question

    )


    return result





# ==============================
# 本地测试
# ==============================


if __name__ == "__main__":


    question = input(
        "请输入问题:"
    )


    result = run_analysis(
        question
    )


    print(
        "\n======分析完成======"
    )


    print(

        result.get(
            "report",
            ""
        )

    )