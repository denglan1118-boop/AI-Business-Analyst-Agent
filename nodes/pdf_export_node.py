import os

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


from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont



from reportlab.lib.pagesizes import A4





def pdf_export_node(state):


    print(
        "\n====== PDF EXPORT NODE ======"
    )



    report = state.get(
        "report",
        ""
    )


    visualization = state.get(
        "visualization",
        {}
    )


    analysis = state.get(
        "analysis_result",
        {}
    )



    # ==========================
    # 路径
    # ==========================


    BASE_DIR = os.path.dirname(

        os.path.dirname(

            os.path.abspath(__file__)

        )

    )


    report_dir=os.path.join(

        BASE_DIR,

        "reports"

    )


    os.makedirs(

        report_dir,

        exist_ok=True

    )



    pdf_path=os.path.join(

        report_dir,

        "customer_sales_report.pdf"

    )



    # ==========================
    # 中文字体
    # ==========================


    font_path = (

        "C:/Windows/Fonts/msyh.ttc"

    )


    if os.path.exists(font_path):


        pdfmetrics.registerFont(

            TTFont(

                "MicrosoftYaHei",

                font_path

            )

        )


        font_name="MicrosoftYaHei"


    else:


        font_name="Helvetica"



    styles=getSampleStyleSheet()



    for style in styles.byName.values():

        style.fontName=font_name




    # ==========================
    # 创建PDF
    # ==========================


    doc=SimpleDocTemplate(

        pdf_path,

        pagesize=A4

    )



    content=[]



    # ==========================
    # 标题
    # ==========================


    content.append(

        Paragraph(

            "AI客户价值与销售趋势商业分析报告",

            styles["Title"]

        )

    )


    content.append(

        Spacer(

            1,

            20

        )

    )



    # ==========================
    # KPI
    # ==========================


    rfm=analysis.get(

        "rfm",

        {}

    )


    sales=analysis.get(

        "sales",

        {}

    )



    kpi_data=[

        [

            "指标",

            "结果"

        ],

        [

            "客户数量",

            str(

                rfm.get(

                    "customer_count",

                    0

                )

            )

        ],

        [

            "订单数量",

            str(

                sales.get(

                    "order_count",

                    0

                )

            )

        ],

        [

            "销售金额",

            f"{sales.get('total_sales',0):,.2f}"

        ]

    ]



    table=Table(

        kpi_data

    )



    table.setStyle(

        TableStyle(

            [

                (

                    "GRID",

                    (0,0),

                    (-1,-1),

                    0.5,

                    None

                )

            ]

        )

    )


    content.append(

        table

    )


    content.append(

        Spacer(

            1,

            20

        )

    )



    # ==========================
    # 报告文字
    # ==========================


    for line in report.split("\n"):


        line=line.strip()



        if not line:

            continue



        content.append(

            Paragraph(

                line,

                styles["BodyText"]

            )

        )


        content.append(

            Spacer(

                1,

                6

            )

        )




    # ==========================
    # 添加图片
    # ==========================


    content.append(

        Paragraph(

            "可视化分析",

            styles["Heading2"]

        )

    )



    for name,path in visualization.items():


        if path and os.path.exists(path):


            content.append(

                Paragraph(

                    name,

                    styles["Heading3"]

                )

            )


            img=Image(

                path,

                width=400,

                height=220

            )


            content.append(

                img

            )


            content.append(

                Spacer(

                    1,

                    20

                )

            )




    # ==========================
    # 生成PDF
    # ==========================


    doc.build(

        content

    )



    print(

        "PDF报告生成完成"

    )


    print(

        pdf_path

    )



    return {


        "pdf_export":{


            "pdf":

            pdf_path,


            "time":

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        }

    }