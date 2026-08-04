import os
import json
from datetime import datetime



def memory_node(state):


    print(
        "\n====== MEMORY NODE ======"
    )



    # =========================
    # 项目根目录
    # =========================


    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )


    memory_dir = os.path.join(
        BASE_DIR,
        "memory"
    )


    os.makedirs(
        memory_dir,
        exist_ok=True
    )


    memory_file = os.path.join(
        memory_dir,
        "history.json"
    )



    # =========================
    # 读取历史
    # =========================


    history=[]


    if os.path.exists(memory_file):


        try:

            with open(
                memory_file,
                "r",
                encoding="utf-8"
            ) as f:


                history=json.load(f)


        except:


            history=[]





    # =========================
    # 当前分析信息
    # =========================


    question = state.get(
        "question",
        ""
    )


    sql = state.get(
        "sql",
        ""
    )


    analysis = state.get(
        "analysis_result",
        {}
    )


    insight = state.get(
        "insight",
        {}
    )


    visualization = state.get(
        "visualization",
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




    # =========================
    # 创建记录
    # =========================


    record={


        "time":

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),



        "question":

        question,



        "sql":

        sql,



        "customer_count":

        rfm.get(
            "customer_count",
            0
        ),



        "total_sales":

        sales.get(
            "total_sales",
            0
        ),



        "order_count":

        sales.get(
            "order_count",
            0
        ),



        "insight":

        insight,



        "visualization":

        visualization

    }




    history.append(
        record
    )




    # =========================
    # 保留最近100次
    # =========================


    history = history[-100:]




    # =========================
    # 保存
    # =========================


    with open(

        memory_file,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            history,

            f,

            ensure_ascii=False,

            indent=4

        )




    print(
        f"历史分析已保存，共 {len(history)} 条"
    )



    return {


        "memory":{


            "current":

            record,


            "history_count":

            len(history)

        }


    }