import pandas as pd

from langchain_core.tools import tool



@tool
def analysis_sales(data:list):

    """
    商业销售分析工具
    """

    df=pd.DataFrame(data)



    result={}


    # 自动识别字段

    if df.shape[1]==2:

        df.columns=[
            "Dimension",
            "Value"
        ]


    elif df.shape[1]==3:

        df.columns=[
            "Dimension",
            "Sales",
            "Profit"
        ]



    result["数据量"]=len(df)



    # ==================
    # 销售分析
    # ==================

    if "Value" in df.columns:


        df=df.sort_values(
            "Value",
            ascending=False
        )


        result["排名"]=(
            df.to_dict(
                orient="records"
            )
        )


        top=df.iloc[0]


        result["最高类别"]={
            "名称":top["Dimension"],
            "金额":float(top["Value"])
        }



        result["总金额"]=round(
            float(df["Value"].sum()),
            2
        )



        result["商业洞察"]=(
            f"{top['Dimension']} "
            f"为最高贡献类别，"
            f"金额达到 {top['Value']}。"
        )



    return result