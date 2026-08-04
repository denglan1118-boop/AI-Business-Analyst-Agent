import os
from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from datetime import datetime

from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle

)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import A4


from api.agent_api import run_agent



REPORT_DIR = "reports"
# ==========================
# 注册中文字体
# ==========================

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"


pdfmetrics.registerFont(

    TTFont(
        "MicrosoftYaHei",
        FONT_PATH
    )

)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)



def create_pdf_report(
        question
):


    # ==========================
    # 调用Agent
    # ==========================

    result = run_agent(
        question
    )


    if result["status"] != "success":

        raise Exception(
            result["message"]
        )


    dashboard = result["dashboard"]


    report_text = result["report"]



    pdf_path = os.path.join(

        REPORT_DIR,

        "business_report.pdf"

    )


    # ==========================
    # 创建PDF
    # ==========================

    doc = SimpleDocTemplate(

        pdf_path,

        pagesize=A4

    )

    styles = getSampleStyleSheet()

    for style_name in styles.byName:
        styles[style_name].fontName = "MicrosoftYaHei"


    story = []



    # ==========================
    # 标题
    # ==========================


    story.append(

        Paragraph(

            "AI Business Analyst 商业分析报告",

            styles["Title"]

        )

    )


    story.append(

        Spacer(
            1,
            20
        )

    )



    story.append(

        Paragraph(

            f"生成时间：{datetime.now()}",

            styles["Normal"]

        )

    )


    story.append(
        Spacer(
            1,
            20
        )
    )



    # ==========================
    # KPI
    # ==========================


    story.append(

        Paragraph(

            "一、核心经营指标",

            styles["Heading2"]

        )

    )



    kpi = dashboard.get(
        "kpi",
        {}
    )


    table_data = [

        [
            "指标",
            "数值"
        ],

        [
            "销售额",
            f"{kpi.get('total_sales',0):,.2f}"
        ],

        [
            "利润",
            f"{kpi.get('total_profit',0):,.2f}"
        ],

        [
            "平均月销售",
            f"{kpi.get('average_monthly_sales',0):,.2f}"
        ],

        [
            "利润率",
            f"{kpi.get('average_profit_margin',0)}%"
        ]

    ]



    table = Table(
        table_data
    )

    table.setStyle(

        TableStyle(

            [

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    None
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "MicrosoftYaHei"
                )

            ]

        )

    )

    story.append(
        table
    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # ==========================
    # 客户分析
    # ==========================


    story.append(

        Paragraph(

            "二、客户价值分析",

            styles["Heading2"]

        )

    )


    customer = dashboard.get(
        "customer",
        {}
    )


    rfm = customer.get(
        "rfm",
        {}
    )


    summary = rfm.get(
        "summary",
        {}
    )


    text = f"""

客户数量：
{summary.get('customer_count',0)}

平均RFM评分：
{summary.get('average_rfm_score',0)}

平均消费金额：
{summary.get('average_monetary',0)}

客户等级：

{summary.get('level_distribution',{})}

"""


    story.append(

        Paragraph(

            text.replace(
                "\n",
                "<br/>"
            ),

            styles["Normal"]

        )

    )



    story.append(
        Spacer(
            1,
            20
        )
    )



    # ==========================
    # 插入图表
    # ==========================


    story.append(

        Paragraph(

            "三、数据可视化",

            styles["Heading2"]

        )

    )



    charts = dashboard.get(
        "charts",
        {}
    )


    for name,path in charts.items():


        if path.startswith(
            "/static/"
        ):

            img_path = path.replace(

                "/static/",

                ""

            )


        else:

            img_path = path



        if os.path.exists(
            img_path
        ):


            story.append(

                Paragraph(

                    name,

                    styles["Heading3"]

                )

            )


            story.append(

                Image(

                    img_path,

                    width=400,

                    height=250

                )

            )


            story.append(

                Spacer(
                    1,
                    15
                )

            )



    # ==========================
    # AI报告
    # ==========================


    story.append(

        Paragraph(

            "四、AI商业洞察",

            styles["Heading2"]

        )

    )


    story.append(

        Paragraph(

            report_text.replace(
                "\n",
                "<br/>"
            ),

            styles["Normal"]

        )

    )



    doc.build(
        story
    )


    return pdf_path