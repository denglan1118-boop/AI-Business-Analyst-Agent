import os
import json
import shutil
from datetime import datetime

import markdown




def export_node(state):


    print(
        "\n====== EXPORT NODE ======"
    )


    # ==========================
    # 获取数据
    # ==========================


    report = state.get(
        "report",
        ""
    )


    analysis = state.get(
        "analysis_result",
        {}
    )


    visualization = state.get(
        "visualization",
        {}
    )


    insight = state.get(
        "insight",
        {}
    )


    chart_summary = state.get(
        "chart_summary",
        {}
    )


    memory = state.get(
        "memory",
        {}
    )



    # ==========================
    # 时间版本
    # ==========================


    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )



    # ==========================
    # 项目目录
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


    image_dir=os.path.join(
        report_dir,
        "images"
    )


    data_dir=os.path.join(
        BASE_DIR,
        "data"
    )



    os.makedirs(
        report_dir,
        exist_ok=True
    )


    os.makedirs(
        image_dir,
        exist_ok=True
    )


    os.makedirs(
        data_dir,
        exist_ok=True
    )

    # ==========================
    # 复制图片
    # ==========================

    image_mapping = {}

    visual_dir = os.path.join(
        BASE_DIR,
        "visualization"
    )

    for name, path in visualization.items():

        if not path:
            continue

        # 处理相对路径

        if not os.path.isabs(path):

            source_path = os.path.join(
                BASE_DIR,
                path
            )

        else:

            source_path = path

        print(
            "检查图片:",
            source_path
        )

        if os.path.exists(source_path):

            filename = os.path.basename(
                source_path
            )

            target_path = os.path.join(
                image_dir,
                filename
            )

            shutil.copy(
                source_path,
                target_path
            )

            image_mapping[name] = (
                    "images/"
                    +
                    filename.replace("\\", "/")
            )


        else:

            print(
                "图片不存在:",
                source_path
            )

    print(
        "最终图片映射:"
    )

    print(
        image_mapping
    )



    print(
        "图片复制完成"
    )



    # ==========================
    # 1. Markdown报告
    # ==========================


    md_path=os.path.join(

        report_dir,

        f"customer_sales_report_{timestamp}.md"

    )

    md_report = report

    for key, value in image_mapping.items():

        old = visualization.get(
            key,
            ""
        )

        if old:
            md_report = md_report.replace(
                old.replace("\\", "/"),
                value
            )

    with open(
            md_path,
            "w",
            encoding="utf-8"
    ) as f:

        f.write(md_report)



    print(
        "Markdown报告导出完成"
    )




    # ==========================
    # 2. HTML报告
    # ==========================



    html_report = report

    # ==========================
    # 替换Markdown图片路径
    # ==========================

    for key, value in image_mapping.items():

        old = visualization.get(
            key,
            ""
        )

        if old:
            old = old.replace(
                "\\",
                "/"
            )

            html_report = html_report.replace(
                old,
                value
            )

            print(
                "替换图片:",
                old,
                "=>",
                value
            )

    html_body = markdown.markdown(

        html_report,

        extensions=[
            "tables",
            "fenced_code",
            "nl2br"
        ]

    )



    html_path=os.path.join(

        report_dir,

        f"customer_sales_report_{timestamp}.html"

    )




    html_content=f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">


<title>
AI商业分析报告
</title>


<style>


body{{

font-family:
Microsoft YaHei;

margin:40px;

line-height:1.8;

background:#fafafa;

}}



h1{{

color:#1f4e79;

}}



table{{

border-collapse:
collapse;

width:90%;

background:white;

}}



th,td{{

border:
1px solid #ddd;

padding:
10px;

}}



img{{

max-width:
900px;

margin:
20px;

}}



</style>


</head>



<body>


{html_body}


</body>


</html>

"""



    with open(

        html_path,

        "w",

        encoding="utf-8"

    ) as f:


        f.write(
            html_content
        )



    print(
        "HTML报告导出完成"
    )





    # ==========================
    # 3. JSON数据
    # ==========================



    json_path=os.path.join(

        data_dir,

        f"analysis_result_{timestamp}.json"

    )




    export_data={


        "analysis":

        analysis,


        "visualization":

        image_mapping,


        "insight":

        insight,


        "chart_summary":

        chart_summary,


        "memory":

        memory,


        "create_time":

        datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )

    }




    with open(

        json_path,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            export_data,

            f,

            ensure_ascii=False,

            indent=4

        )



    print(
        "JSON数据导出完成"
    )




    print(
        "\n报告目录:"
    )


    print(
        report_dir
    )



    return {


        "export":{


            "markdown":

            md_path,


            "html":

            html_path,


            "json":

            json_path,


            "images":

            image_mapping


        }

    }