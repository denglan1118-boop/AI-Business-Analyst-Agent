import pandas as pd
from langchain_core.tools import tool

@tool
def detect_profit_anomaly(data:list):


    df=pd.DataFrame(data)


    df.columns=[
        "Product",
        "Profit"
    ]


    threshold = (
        df["Profit"]
        .mean()
        -
        df["Profit"]
        .std()
    )


    bad=df[
        df["Profit"]
        <
        threshold
    ]


    return {

        "risk_products":
        bad.to_dict(
            orient="records"
        )

    }