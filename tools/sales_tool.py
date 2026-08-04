import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

from langchain_core.tools import tool


matplotlib.rcParams["font.sans-serif"] = [
    "SimHei"
]

matplotlib.rcParams["axes.unicode_minus"] = False


@tool
def analyze_sales(data: list):
    """
    销售趋势分析工具

    输入:
    [
        Customer ID,
        Customer Name,
        Order Date,
        Sales
    ]

    输出:
    销售趋势
    月度销售
    可视化
    """

    # ======================
    # 兼容不同输入格式
    # ======================

    if isinstance(data, dict):

        rows = data["data"]

    else:

        rows = data

    # ======================
    # 自动识别数据类型
    # ======================

    if len(rows) == 0:
        return {
            "error": "没有查询结果"
        }

    # RFM查询结果
    # Customer ID
    # Customer Name
    # Last_Date
    # Frequency
    # Monetary

    if len(rows[0]) == 5:

        print(
            "识别为RFM数据"
        )

        df = pd.DataFrame(

            rows,

            columns=[

                "Customer ID",

                "Customer Name",

                "Last_Date",

                "Frequency",

                "Monetary"

            ]

        )

        df["Last_Date"] = pd.to_datetime(

            df["Last_Date"]

        )

        df["Frequency"] = pd.to_numeric(

            df["Frequency"]

        )

        df["Monetary"] = pd.to_numeric(

            df["Monetary"]

        )


    # 订单明细数据
    # Customer ID
    # Customer Name
    # Order Date
    # Sales

    elif len(rows[0]) == 4:

        print(
            "识别为订单明细数据"
        )

        df = pd.DataFrame(

            rows,

            columns=[

                "Customer ID",

                "Customer Name",

                "Order Date",

                "Sales"

            ]

        )

        df["Order Date"] = pd.to_datetime(

            df["Order Date"]

        )

        df["Sales"] = pd.to_numeric(

            df["Sales"]

        )


    else:

        raise ValueError(

            f"未知数据格式，字段数量:{len(rows[0])}"

        )



    # =========================
    # 月销售趋势
    # =========================


    df["Month"] = (
        df["Order Date"]
        .dt
        .to_period("M")
        .astype(str)
    )


    monthly_sales = (

        df
        .groupby("Month")
        ["Sales"]
        .sum()
        .reset_index()

    )

    # ===================
    # 年销售统计
    # ===================

    df["Year"] = (
        df["Order Date"]
        .dt
        .year
    )

    yearly_sales = (

        df
        .groupby("Year")
        ["Sales"]
        .sum()
        .reset_index()

    )

    yearly_sales["Sales"] = (
        yearly_sales["Sales"]
        .round(2)
    )

    max_month = (

        monthly_sales
        .sort_values(
            "Sales",
            ascending=False
        )
        .iloc[0]
        .to_dict()

    )



    min_month = (

        monthly_sales
        .sort_values(
            "Sales"
        )
        .iloc[0]
        .to_dict()

    )



    # =========================
    # 图片
    # =========================


    os.makedirs(
        "visualization",
        exist_ok=True
    )


    plt.figure(
        figsize=(12,5)
    )


    plt.plot(
        monthly_sales["Month"],
        monthly_sales["Sales"],
        marker="o"
    )


    plt.xticks(
        rotation=45
    )


    plt.title(
        "Monthly Sales Trend"
    )


    plt.xlabel(
        "Month"
    )


    plt.ylabel(
        "Sales"
    )


    plt.tight_layout()



    plt.savefig(
        "visualization/monthly_sales_trend.png",
        dpi=300
    )


    plt.close()



    return {


        "total_sales":
            float(
                round(
                    df["Sales"].sum(),
                    2
                )
            ),


        "order_count":
        len(df),

        "max_sales_yearly":
            max_month,

        "min_sales_yearly":
            min_month,

        "yearly_sales":

            yearly_sales.to_dict(
                orient="records"
            ),

        "max_sales_month":
        max_month,


        "min_sales_month":
        min_month,



        "monthly_sales":

        monthly_sales.to_dict(
            orient="records"
        ),



        "visualization":
        {
            "monthly_sales_trend":
            "visualization/monthly_sales_trend.png"
        }

    }