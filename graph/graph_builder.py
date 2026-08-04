from typing import TypedDict, Any, Optional

from langgraph.graph import StateGraph, END


from nodes.sql_node import sql_node
from nodes.execute_node import execute_node
from nodes.validation_node import validation_node
from nodes.correction_node import correction_node
from nodes.analysis_node import analysis_node
from nodes.visualization_node import visualization_node
from nodes.chart_summary_node import chart_summary_node
from nodes.memory_node import memory_node
from nodes.insight_node import insight_node
from nodes.report_node import report_node
from nodes.export_node import export_node
from nodes.pdf_export_node import pdf_export_node
from nodes.excel_export_node import excel_export_node


# ==========================
# Agent状态
# ==========================

class AgentState(TypedDict):

    question: str

    sql: str

    raw_data: Any


    analysis_result: dict


    validation: str


    error: Optional[str]


    retry_count: int



    # 可视化结果

    visualization: dict



    # 图表摘要

    chart_summary: dict



    # AI洞察

    insight: dict



    # 历史记忆

    memory: dict



    # 报告

    report: str



    # 导出结果

    export: dict

    pdf_export: dict





# ==========================
# 构建Graph
# ==========================


def build_graph():


    graph = StateGraph(
        AgentState
    )



    # ==========================
    # 添加节点
    # ==========================


    graph.add_node(
        "sql",
        sql_node
    )


    graph.add_node(
        "execute",
        execute_node
    )


    graph.add_node(
        "validation",
        validation_node
    )


    graph.add_node(
        "correction",
        correction_node
    )


    graph.add_node(
        "analysis",
        analysis_node
    )


    graph.add_node(
        "visualization",
        visualization_node
    )


    # 新增图表总结节点

    graph.add_node(
        "chart_summary",
        chart_summary_node
    )



    # 新增记忆节点

    graph.add_node(
        "memory",
        memory_node
    )



    graph.add_node(
        "insight",
        insight_node
    )


    graph.add_node(
        "report",
        report_node
    )


    graph.add_node(
        "export",
        export_node
    )

    graph.add_node(
        "pdf_export",
        pdf_export_node
    )

    graph.add_node(
        "excel_export",
        excel_export_node
    )



    # ==========================
    # 设置入口
    # ==========================


    graph.set_entry_point(
        "sql"
    )





    # ==========================
    # SQL流程
    # ==========================


    graph.add_edge(
        "sql",
        "execute"
    )


    graph.add_edge(
        "execute",
        "validation"
    )





    # ==========================
    # SQL验证分支
    # ==========================


    graph.add_conditional_edges(

        "validation",

        lambda state:
        state["validation"],


        {

            "pass":
            "analysis",


            "failed":
            "correction"

        }

    )





    # ==========================
    # SQL修正循环
    # ==========================


    graph.add_edge(

        "correction",

        "sql"

    )





    # ==========================
    # AI分析流程
    # ==========================


    graph.add_edge(
        "analysis",
        "visualization"
    )



    graph.add_edge(
        "visualization",
        "chart_summary"
    )



    graph.add_edge(
        "chart_summary",
        "memory"
    )



    graph.add_edge(
        "memory",
        "insight"
    )

    graph.add_edge(
        "insight",
        "report"
    )

    graph.add_edge(
        "report",
        "export"
    )

    graph.add_edge(
        "export",
        "excel_export"
    )

    graph.add_edge(
        "excel_export",
        "pdf_export"
    )

    graph.add_edge(
        "pdf_export",
        END
    )





    return graph.compile()