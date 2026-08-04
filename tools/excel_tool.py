import pandas as pd

import os

from langchain_core.tools import tool



BASE_DIR=os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


REPORT_DIR=os.path.join(
    BASE_DIR,
    "reports"
)


os.makedirs(
    REPORT_DIR,
    exist_ok=True
)



@tool
def generate_excel_report(
    data:list,
    filename:str="business_report.xlsx"
):


    """
    自动生成Excel商业分析报告
    """



    df=pd.DataFrame(data)



    path=os.path.join(
        REPORT_DIR,
        filename
    )



    with pd.ExcelWriter(
        path,
        engine="openpyxl"
    ) as writer:


        df.to_excel(
            writer,
            sheet_name="Analysis",
            index=False
        )


    return path