import os

import pandas as pd



EXPORT_DIR = "exports"



os.makedirs(
    EXPORT_DIR,
    exist_ok=True
)




def generate_excel_report(data):

    """
    生成AI商业分析Excel报告


    输入:
    dashboard数据


    输出:
    Excel路径

    """



    file_path = os.path.join(

        EXPORT_DIR,

        "AI_Business_Report.xlsx"

    )




    with pd.ExcelWriter(

        file_path,

        engine="openpyxl"

    ) as writer:



        # ==========================
        # KPI
        # ==========================

        kpi = data.get(

            "kpi",

            {}

        )


        if kpi:


            kpi_df = pd.DataFrame(

                [

                    {

                        "指标":

                            k,

                        "数值":

                            v

                    }

                    for k,v in kpi.items()

                ]

            )


            kpi_df.to_excel(

                writer,

                sheet_name="KPI指标",

                index=False

            )





        # ==========================
        # Top10客户
        # ==========================


        customer = data.get(

            "customer",

            {}

        )


        rfm = customer.get(

            "rfm",

            {}

        )



        top10 = rfm.get(

            "top10_customer",

            []

        )



        if top10:



            top_df = pd.DataFrame(

                top10

            )


            top_df.to_excel(

                writer,

                sheet_name="Top10客户",

                index=False

            )






        # ==========================
        # RFM分层
        # ==========================


        level = rfm.get(

            "level_distribution",

            {}

        )



        if level:


            level_df = pd.DataFrame(

                [

                    {

                        "客户等级":

                            k,

                        "数量":

                            v

                    }

                    for k,v in level.items()

                ]

            )


            level_df.to_excel(

                writer,

                sheet_name="RFM分层",

                index=False

            )







        # ==========================
        # 销售趋势
        # ==========================


        sales = data.get(

            "sales",

            {}

        )



        yearly = sales.get(

            "yearly_sales",

            {}

        )



        if yearly:



            year_df = pd.DataFrame(

                [

                    {

                        "年份":

                            k,

                        "销售额":

                            v

                    }

                    for k,v in yearly.items()

                ]

            )



            year_df.to_excel(

                writer,

                sheet_name="年度销售",

                index=False

            )




    return file_path