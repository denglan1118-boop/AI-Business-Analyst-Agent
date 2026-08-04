from agents.sql_agent import agent

import json
import traceback



def run_agent(question):

    try:

        result = agent.invoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":question
                    }
                ]
            }
        )


        messages = result.get(
            "messages",
            []
        )


        answer = ""


        analysis = {

            "kpi": {},

            "customer": {},

            "sales": {},

            "charts": {}

        }



        print("\n====== MESSAGE COUNT ======")
        print(len(messages))


        # ==========================
        # 获取LLM报告
        # ==========================

        if messages:

            last = messages[-1]

            if hasattr(
                last,
                "content"
            ):

                answer = last.content



        # ==========================
        # 提取Tool结果
        # ==========================

        for msg in messages:


            if not hasattr(
                msg,
                "content"
            ):

                continue


            content = msg.content


            if not isinstance(
                content,
                str
            ):

                continue


            try:

                data = json.loads(
                    content
                )

            except:

                continue



            if not isinstance(
                data,
                dict
            ):

                continue



            print(
                "\n====== TOOL KEYS ======"
            )

            print(
                data.keys()
            )



            # ==========================
            # RFM
            # ==========================

            # ==========================
            # RFM
            # ==========================

            if (
                    "summary" in data
                    and
                    isinstance(data["summary"], dict)
            ):

                analysis["customer"]["rfm"] = data["summary"]

                print(
                    "RFM summary loaded"
                )




            # ==========================
            # Sales
            # ==========================

            elif "total_sales" in data:


                analysis["sales"].update(
                    data
                )


                for k in [

                    "total_sales",

                    "total_profit",

                    "average_monthly_sales",

                    "average_profit_margin",

                    "month_count"

                ]:


                    if k in data:

                        analysis["kpi"][k]=data[k]





            # ==========================
            # SQL原始数据
            # 丢弃
            # ==========================

            elif (

                "row_count" in data

                and

                "data" in data

            ):

                continue




            else:

                analysis.update(
                    data
                )




        # ==========================
        # State补充
        # ==========================

        for key in [

            "sales_trend",

            "customer_analysis",

            "visualization"

        ]:


            if key in result:

                analysis[key]=result[key]





        # ==========================
        # 图表整理
        # ==========================

        sales = analysis.get(
            "sales",
            {}
        )


        if "sales_chart" in sales:


            analysis["charts"]["sales_trend"] = (

                sales.pop(
                    "sales_chart"
                )

            )


        if "profit_chart" in sales:


            analysis["charts"]["profit_trend"] = (

                sales.pop(
                    "profit_chart"
                )

            )




        # RFM图片

        # ==========================
        # RFM图表
        # ==========================

        rfm_summary = (

            analysis
            .get(
                "customer",
                {}
            )
            .get(
                "rfm",
                {}
            )

        )

        if isinstance(
                rfm_summary,
                dict
        ):

            for key in [

                "rfm_3d_scatter",

                "rfm_scatter",

                "customer_level_pie"

            ]:

                if key in rfm_summary:
                    analysis["charts"][key] = (

                        rfm_summary[key]

                    )

        if "rfm_3d_scatter" in rfm_summary:
            analysis["charts"]["rfm_scatter"] = (

                rfm_summary["rfm_3d_scatter"]

            )



        # ==========================
        # 图片路径转换
        # ==========================

        def convert_path(obj):


            if isinstance(
                obj,
                dict
            ):

                return {

                    k:convert_path(v)

                    for k,v in obj.items()

                }



            if isinstance(
                obj,
                list
            ):

                return [

                    convert_path(i)

                    for i in obj

                ]



            if isinstance(
                obj,
                str
            ):


                obj=obj.replace(
                    "\\",
                    "/"
                )


                root="D:/AI-Projects/AI-Business-Analyst-Agent/"


                if root in obj:

                    obj=obj.replace(
                        root,
                        ""
                    )


                if obj.endswith(
                    ".png"
                ):


                    if not obj.startswith(
                        "/static/"
                    ):

                        obj="/static/"+obj



            return obj




        analysis = convert_path(
            analysis
        )



        # ==========================
        # 删除空字段
        # ==========================


        analysis={

            k:v

            for k,v in analysis.items()

            if v

        }



        print(
            "\n====== FINAL ======"
        )

        print(
            analysis.keys()
        )

        # ==========================
        # Dashboard 数据整理
        # ==========================

        dashboard = {

            "kpi": analysis.get(
                "kpi",
                {}
            ),

            "customer": {},

            "sales": analysis.get(
                "sales",
                {}
            ),

            "charts": analysis.get(
                "charts",
                {}

            )

        }

        # ==========================
        # 提取RFM数据
        # ==========================

        rfm = (

            analysis
            .get(
                "customer",
                {}
            )
            .get(
                "rfm",
                {}
            )
        )

        if rfm:
            dashboard["customer"] = {

                "customer_count":

                    rfm.get(
                        "customer_count",
                        0
                    ),

                "level_distribution":

                    rfm.get(
                        "level_distribution",
                        {}
                    ),

                "average_rfm_score":

                    rfm.get(
                        "average_rfm_score",
                        0
                    ),

                "average_monetary":

                    rfm.get(
                        "average_monetary",
                        0
                    ),

                "top10_customer":

                    rfm.get(
                        "top10_customer",
                        []
                    )

            }

        return {

            "status":

                "success",

            "question":

                question,

            "report":

                answer,

            "dashboard":

                dashboard

        }




    except Exception as e:


        traceback.print_exc()


        return {


            "status":"error",


            "question":question,


            "message":str(e)

        }