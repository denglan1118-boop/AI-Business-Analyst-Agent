import pandas as pd
import os
from datetime import datetime


def excel_export_node(state):


    print(
        "\n====== EXCEL EXPORT NODE ======"
    )


    analysis = state.get(
        "analysis_result",
        {}
    )


    rfm = analysis.get(
        "rfm",
        {}
    )


    sales = analysis.get(
        "sales",
        {}
    )



    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )


    report_dir = os.path.join(
        BASE_DIR,
        "reports"
    )


    os.makedirs(
        report_dir,
        exist_ok=True
    )


    excel_path = os.path.join(
        report_dir,
        "customer_sales_analysis.xlsx"
    )



    # ==========================
    # 1. Summary
    # ==========================


    summary_df = pd.DataFrame(
        {
            "指标":[
                "客户数量",
                "订单数量",
                "累计销售额",
                "最高销售月份",
                "最高销售额",
                "最低销售月份",
                "最低销售额"
            ],

            "结果":[

                rfm.get(
                    "customer_count",
                    0
                ),

                sales.get(
                    "order_count",
                    0
                ),

                sales.get(
                    "total_sales",
                    0
                ),

                sales.get(
                    "max_month",
                    {}
                ).get(
                    "Month"
                ),

                sales.get(
                    "max_month",
                    {}
                ).get(
                    "Sales"
                ),

                sales.get(
                    "min_month",
                    {}
                ).get(
                    "Month"
                ),

                sales.get(
                    "min_month",
                    {}
                ).get(
                    "Sales"
                )

            ]
        }
    )



    # ==========================
    # 2. Top10客户
    # ==========================


    top10_df = pd.DataFrame(
        rfm.get(
            "top_customer",
            []
        )
    )



    # ==========================
    # 3. RFM分析
    # ==========================


    rfm_df = pd.DataFrame(
        rfm.get(
            "rfm_detail",
            []
        )
    )



    # ==========================
    # 4. 月销售
    # ==========================


    monthly_df = pd.DataFrame(
        sales.get(
            "monthly_sales",
            []
        )
    )



    # ==========================
    # 5. 产品类别
    # ==========================


    category_df = pd.DataFrame(
        sales.get(
            "category_sales",
            []
        )
    )



    # ==========================
    # 6. 地区销售
    # ==========================


    region_df = pd.DataFrame(
        sales.get(
            "region_sales",
            []
        )
    )



    # ==========================
    # 7. 客户分层
    # ==========================


    segment_df = pd.DataFrame(
        [
            {
                "客户类型":k,
                "数量":v
            }

            for k,v in
            rfm.get(
                "level_count",
                {}
            ).items()
        ]
    )



    # ==========================
    # 写入Excel多个Sheet
    # ==========================


    with pd.ExcelWriter(
        excel_path,
        engine="openpyxl"
    ) as writer:


        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )


        top10_df.to_excel(
            writer,
            sheet_name="Top10_Customers",
            index=False
        )


        rfm_df.to_excel(
            writer,
            sheet_name="RFM_Analysis",
            index=False
        )


        monthly_df.to_excel(
            writer,
            sheet_name="Monthly_Sales",
            index=False
        )


        category_df.to_excel(
            writer,
            sheet_name="Category_Sales",
            index=False
        )


        region_df.to_excel(
            writer,
            sheet_name="Region_Sales",
            index=False
        )


        segment_df.to_excel(
            writer,
            sheet_name="Customer_Segment",
            index=False
        )



    print(
        "Excel导出完成:"
    )

    print(
        excel_path
    )


    return {

        "excel_export":
        excel_path

    }