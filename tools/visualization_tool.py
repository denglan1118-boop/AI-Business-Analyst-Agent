import os

import matplotlib

# 非GUI模式，避免Agent线程调用时报错
matplotlib.use("Agg")

import matplotlib.pyplot as plt

import pandas as pd

from langchain_core.tools import tool



# =========================
# 项目路径
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)



CHART_DIR = os.path.join(
    BASE_DIR,
    "charts"
)


os.makedirs(
    CHART_DIR,
    exist_ok=True
)




# ==================================================
# 柱状图
# ==================================================

@tool
def create_bar_chart(data:list):
    """
    根据分类数据生成柱状图。


    适用于:

    Category + Sales

    Category + Profit

    Region + Sales

    Sub-Category + Sales


    输入:

    [
        ("Technology",893633),
        ("Furniture",764284)
    ]


    返回:
    图表路径
    """



    df = pd.DataFrame(
        data,
        columns=[
            "Dimension",
            "Value"
        ]
    )



    plt.figure(
        figsize=(10,5)
    )



    plt.bar(
        df["Dimension"],
        df["Value"]
    )



    plt.xlabel(
        "Dimension"
    )


    plt.ylabel(
        "Value"
    )



    plt.title(
        "Sales Analysis"
    )



    plt.xticks(
        rotation=45
    )



    plt.tight_layout()



    save_path=os.path.join(
        CHART_DIR,
        "sales_bar_chart.png"
    )



    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()



    return save_path





# ==================================================
# 折线趋势图
# ==================================================

@tool
def create_line_chart(data:list):
    """
    根据时间序列数据生成折线图。


    用于:

    Month + Sales

    Year + Sales

    Date + Sales


    输入:

    [
        ("2014-01",14236),
        ("2014-02",4519)
    ]


    返回:
    图表路径

    """



    months = [
        x[0]
        for x in data
    ]


    sales = [
        x[1]
        for x in data
    ]



    plt.figure(
        figsize=(12,5)
    )



    plt.plot(
        months,
        sales,
        marker="o"
    )



    plt.xlabel(
        "Month"
    )


    plt.ylabel(
        "Sales"
    )


    plt.title(
        "Monthly Sales Trend"
    )



    plt.xticks(
        rotation=45
    )



    plt.grid(
        True
    )



    plt.tight_layout()



    save_path=os.path.join(
        CHART_DIR,
        "monthly_sales_trend.png"
    )



    plt.savefig(
        save_path,
        dpi=300,
        bbox_inches="tight"
    )



    plt.close()



    return save_path


