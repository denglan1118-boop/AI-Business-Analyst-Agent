def chart_summary_node(state):


    print(
        "\n====== CHART SUMMARY NODE ======"
    )


    analysis = state.get(
        "analysis_result",
        {}
    )


    visualization = state.get(
        "visualization",
        {}
    )


    sales = analysis.get(
        "sales",
        {}
    )


    rfm = analysis.get(
        "rfm",
        {}
    )



    summary = {}



    # =====================
    # 销售趋势图分析
    # =====================


    monthly_sales = sales.get(
        "monthly_sales",
        []
    )


    if monthly_sales:


        first = monthly_sales[0]["Sales"]

        last = monthly_sales[-1]["Sales"]


        if last > first:

            trend = "销售整体呈增长趋势"

        elif last < first:

            trend = "销售整体呈下降趋势"

        else:

            trend = "销售保持稳定"



        max_month = sales.get(
            "max_month",
            {}
        )


        summary["sales_chart"] = f"""

销售趋势分析：

{trend}。

最高销售月份为：
{max_month.get("Month")}

销售额达到：
{max_month.get("Sales",0):,.2f} 元。

从长期趋势来看，
企业销售存在明显周期波动，
建议结合旺季提前制定营销策略。

"""


    else:

        summary["sales_chart"] = ""




    # =====================
    # 客户分层分析
    # =====================


    level_count = rfm.get(
        "level_count",
        {}
    )


    if level_count:


        high = level_count.get(
            "高价值客户",
            0
        )


        total = sum(
            level_count.values()
        )


        ratio = (

            high /
            total *
            100

            if total

            else 0

        )


        summary["segment_chart"] = f"""


客户分层分析：

当前共有 {total} 名客户。

其中高价值客户：

{high} 人

占比：

{ratio:.1f}%


企业客户存在明显价值分层，
需要重点维护高价值客户，
同时提升潜力客户转化率。

"""


    else:

        summary["segment_chart"] = ""





    # =====================
    # Top客户分析
    # =====================


    top_customer = rfm.get(
        "top_customer",
        []
    )


    if top_customer:


        top1 = top_customer[0]


        summary["top_customer_chart"] = f"""


Top10客户分析：

最高价值客户：

{top1['Customer Name']}


累计消费：

{top1['Monetary']:,.2f} 元


核心客户贡献明显，
建议建立VIP客户运营机制。

"""


    else:

        summary["top_customer_chart"] = ""




    print(
        "图表分析完成"
    )



    return {


        "chart_summary":

        summary


    }