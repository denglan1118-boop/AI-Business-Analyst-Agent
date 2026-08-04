import os

import matplotlib

# 防止线程GUI错误
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from langchain_core.tools import tool



# ==========================
# 路径
# ==========================

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



# =====================================================
# 销售趋势分析工具
# =====================================================


@tool
def analyze_sales_trend(data:list):
    """
    分析时间序列销售趋势。


    支持:

    Month + Sales

    Month + Sales + Profit

    Month + Sales + Profit + Quantity



    输入:

    [
        ("2014-01",14236),
        ("2014-02",4519)
    ]



    返回:

    销售趋势分析报告
    """



    # ==========================
    # DataFrame
    # ==========================


    df = pd.DataFrame(data)

    print("====================")
    print(df.head())
    print(df.columns)
    print(df.shape)

    for col in df.columns:
        print(
            col,
            df[col].astype(str).str.len().max()
        )

    print("====================")

    # ==========================
    # 兼容SQL别名
    # ==========================

    df.rename(
        columns={
            "Total Sales": "Sales",
            "Total Profit": "Profit",
            "Total Quantity": "Quantity"
        },
        inplace=True
    )

    # ==========================
    # 自动识别字段
    # ==========================


    if df.shape[1] == 2:

        df.columns = [

            "Month",
            "Sales"

        ]


    elif df.shape[1] == 3:

        df.columns = [

            "Month",
            "Sales",
            "Profit"

        ]


    elif df.shape[1] == 4:

        df.columns = [

            "Month",
            "Sales",
            "Profit",
            "Quantity"

        ]


    else:

        return {

            "error":
            "不支持的数据格式"

        }

    result = {}

    # ==========================
    # 数据清洗
    # ==========================

    df["Month"] = df["Month"].astype(str)

    df["Sales"] = pd.to_numeric(
        df["Sales"],
        errors="coerce"
    )

    if "Profit" in df.columns:
        df["Profit"] = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        )

    df = df.dropna()

    # 防止异常超长坐标
    df["Month"] = df["Month"].str[:7]

    print("清洗后:")
    print(df.head())
    print(df.dtypes)



    # ==========================
    # 基础销售指标
    # ==========================


    total_sales = df["Sales"].sum()


    avg_sales = df["Sales"].mean()



    result["total_sales"] = round(
        float(total_sales),
        2
    )


    result["average_monthly_sales"] = round(
        float(avg_sales),
        2
    )



    result["month_count"] = len(df)



    # ==========================
    # 最高最低销售月份
    # ==========================


    max_sales=df.loc[
        df["Sales"].idxmax()
    ]


    min_sales=df.loc[
        df["Sales"].idxmin()
    ]



    result["best_month"]={

        "month":
        max_sales["Month"],


        "sales":
        round(
            float(max_sales["Sales"]),
            2
        )

    }



    result["worst_month"]={

        "month":
        min_sales["Month"],


        "sales":
        round(
            float(min_sales["Sales"]),
            2
        )

    }



    # ==================================================
    # 年度销售分析
    # ==================================================


    df["Year"] = (
        df["Month"]
        .astype(str)
        .str[:4]
    )



    yearly_sales=(

        df
        .groupby("Year")
        ["Sales"]
        .sum()

    )



    yearly_growth={}


    years=list(
        yearly_sales.index
    )



    for i,year in enumerate(years):


        sales=float(
            yearly_sales[year]
        )


        if i==0:

            yearly_growth[year]={

                "sales":
                round(
                    sales,
                    2
                ),

                "growth":
                None

            }


        else:


            previous=float(
                yearly_sales[
                    years[i-1]
                ]
            )


            growth=(

                sales-previous

            )/previous*100



            yearly_growth[year]={

                "sales":
                round(
                    sales,
                    2
                ),


                "growth":

                round(
                    growth,
                    2
                )

            }



    result["yearly_sales"]=yearly_growth



    # ==================================================
    # 利润分析
    # ==================================================


    if "Profit" in df.columns:


        total_profit=df["Profit"].sum()



        result["total_profit"]=round(

            float(total_profit),

            2

        )



        # 利润率


        df["Profit_Margin"]=(

            df["Profit"]

            /

            df["Sales"]

            *

            100

        )



        avg_margin=df[
            "Profit_Margin"
        ].mean()



        result["average_profit_margin"]=round(

            float(avg_margin),

            2

        )



        # 最大利润月份


        max_profit=df.loc[

            df["Profit"].idxmax()

        ]



        result["best_profit_month"]={


            "month":

            max_profit["Month"],



            "profit":

            round(

                float(
                    max_profit["Profit"]
                ),

                2

            )

        }




        # 最低利润率


        min_margin=df.loc[

            df["Profit_Margin"].idxmin()

        ]



        result["lowest_profit_margin_month"]={


            "month":

            min_margin["Month"],



            "margin":

            round(

                float(
                    min_margin["Profit_Margin"]
                ),

                2

            )

        }

    # ==================================================
    # 数据处理
    # ==================================================

    # SQL返回字段兼容
    if "Total_Sales" in df.columns:
        df["Sales"] = df["Total_Sales"]

    if "Total_Profit" in df.columns:
        df["Profit"] = df["Total_Profit"]

    # 防止Month异常导致matplotlib生成超大图片
    df["Month"] = df["Month"].astype(str)

    # 排序
    df = df.sort_values(
        by="Month"
    )

    # 防止异常数据
    df = df.head(100)

    # ==================================================
    # 销售趋势图
    # ==================================================

    plt.figure(
        figsize=(12, 5)
    )

    plt.plot(
        range(len(df)),
        df["Sales"],
        marker="o",
        label="Sales"
    )

    plt.xticks(
        range(len(df)),
        df["Month"],
        rotation=45
    )

    plt.title(
        "Sales Trend"
    )

    plt.legend()

    plt.tight_layout()

    sales_chart = os.path.join(

        CHART_DIR,

        "sales_trend.png"

    )

    plt.savefig(

        sales_chart,

        dpi=300,

        bbox_inches="tight",

        pad_inches=0.2

    )

    plt.close()

    # ==================================================
    # 销售+利润双折线
    # ==================================================

    if "Profit" in df.columns:
        plt.figure(
            figsize=(12, 5)
        )

        plt.plot(
            range(len(df)),
            df["Sales"],
            marker="o",
            label="Sales"
        )

        plt.xticks(
            range(len(df)),
            df["Month"],
            rotation=45
        )

        plt.legend()

        plt.xticks(
            rotation=45
        )

        plt.title(
            "Sales and Profit Trend"
        )

        plt.tight_layout()

        profit_chart = os.path.join(

            CHART_DIR,

            "sales_profit_trend.png"

        )

        plt.savefig(

            profit_chart,

            dpi=300,

            bbox_inches="tight",

            pad_inches=0.2

        )

        plt.close()

        result["profit_chart"] = profit_chart

    result["sales_chart"] = sales_chart

    return result