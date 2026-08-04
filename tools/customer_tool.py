import pandas as pd
from langchain_core.tools import tool


@tool
def analyze_customer(data:list):

    df=pd.DataFrame(data)


    df.columns=[
        "Customer",
        "Sales"
    ]


    top_customer=(
        df.sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )


    return {

        "Top10_customer":
        top_customer.to_dict(
            orient="records"
        ),

        "highest_customer":
        top_customer.iloc[0].to_dict()

    }