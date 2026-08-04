from langchain_core.tools import tool



@tool
def format_sql_result(data):
    """
    保留SQL原始结果。

    提供给后续分析工具。
    """


    return data