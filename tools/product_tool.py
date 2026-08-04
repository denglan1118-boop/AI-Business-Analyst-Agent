import pandas as pd

from langchain_core.tools import tool



@tool
def analyze_top_products(data:list):
    """
    Top产品分析工具


    输入:

    [
    (
    Product Name,
    Category,
    Sub-Category,
    Sales,
    Profit,
    Quantity
    )
    ]


    输出:

    - Top产品排名
    - 总销售额
    - 总利润
    - 最佳产品
    - 商业洞察

    """



    # =========================
    # 创建DataFrame
    # =========================


    df=pd.DataFrame(
        data,
        columns=[
            "Product Name",
            "Category",
            "Sub-Category",
            "Sales",
            "Profit",
            "Quantity"
        ]
    )



    result={}



    # =========================
    # 基础指标
    # =========================


    result["product_count"]=len(df)



    result["total_sales"]=round(
        df["Sales"].sum(),
        2
    )


    result["total_profit"]=round(
        df["Profit"].sum(),
        2
    )



    # =========================
    # 排名
    # =========================


    ranking=(

        df
        .sort_values(
            "Sales",
            ascending=False
        )
        [
            [
                "Product Name",
                "Category",
                "Sub-Category",
                "Sales",
                "Profit",
                "Quantity"
            ]
        ]
        .to_dict(
            orient="records"
        )

    )


    result["top_products"]=ranking




    # =========================
    # 第一名产品
    # =========================


    top=df.iloc[0]


    result["best_product"]={

        "name":
        top["Product Name"],

        "sales":
        float(top["Sales"]),

        "profit":
        float(top["Profit"])

    }



    # =========================
    # 类别贡献
    # =========================


    category_sales=(

        df
        .groupby(
            "Category"
        )["Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .to_dict()

    )


    result["category_sales"]=category_sales



    # =========================
    # 商业洞察
    # =========================


    insights=[]



    insights.append(
        f"Top10产品累计销售额为 {result['total_sales']:.2f}"
    )



    insights.append(
        f"销售额最高产品为 {top['Product Name']}，"
        f"销售额 {top['Sales']:.2f}"
    )



    if top["Profit"] < 0:

        insights.append(
            "最高销售产品存在亏损，需要关注成本和定价策略"
        )


    else:

        insights.append(
            "最高销售产品同时保持盈利，具有较高商业价值"
        )



    result["insights"]=insights



    return result