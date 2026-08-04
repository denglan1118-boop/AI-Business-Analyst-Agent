def insight_node(state):


    print(
        "\n====== INSIGHT NODE ======"
    )


    analysis = state.get(
        "analysis_result",
        {}
    )


    insights = {}



    # ==========================
    # 客户分析
    # ==========================


    rfm = analysis.get(
        "rfm",
        {}
    )


    level_count = rfm.get(
        "level_count",
        {}
    )


    customer_count = rfm.get(
        "customer_count",
        0
    )


    high_value = level_count.get(
        "高价值客户",
        0
    )


    potential = level_count.get(
        "潜力客户",
        0
    )


    if customer_count:


        high_ratio = (

            high_value /
            customer_count

            *

            100

        )


    else:

        high_ratio = 0



    if high_ratio < 30:


        customer_insight = (

            "高价值客户占比较低，"
            "需要加强客户维护，提高客户生命周期价值。"

        )


    else:


        customer_insight = (

            "高价值客户占比较高，"
            "企业客户结构较健康。"

        )



    insights["customer"] = customer_insight



    # ==========================
    # Top客户贡献
    # ==========================


    top_customer = rfm.get(
        "top_customer",
        []
    )


    total_top_sales = 0


    for c in top_customer:

        total_top_sales += (
            c["Monetary"]
        )



    sales = analysis.get(
        "sales",
        {}
    )


    total_sales = sales.get(
        "total_sales",
        0
    )



    if total_sales:


        concentration=(

            total_top_sales /
            total_sales
            *
            100

        )


    else:

        concentration=0



    if concentration > 20:


        concentration_insight=(

            "销售收入集中于少数核心客户，"
            "存在客户依赖风险。"

        )


    else:


        concentration_insight=(

            "客户贡献较分散，"
            "收入结构较稳定。"

        )



    insights["customer_concentration"] = (

        concentration_insight

    )



    # ==========================
    # 销售趋势
    # ==========================


    monthly_sales = sales.get(
        "monthly_sales",
        []
    )


    if len(monthly_sales)>=2:


        first = monthly_sales[0]["Sales"]

        last = monthly_sales[-1]["Sales"]


        growth=(

            last-first

        )/first*100



        if growth > 0:


            sales_insight=(

                f"整体销售呈增长趋势，"
                f"首末月份增长{growth:.2f}%。"

            )


        else:


            sales_insight=(

                "整体销售趋势下降，"
                "需要关注市场变化。"

            )


    else:


        sales_insight="销售数据不足"



    insights["sales"] = sales_insight



    # ==========================
    # 行动建议
    # ==========================


    actions=[


        "针对高价值客户建立VIP维护体系",


        "针对潜力客户开展精准营销和复购提升",


        "结合销售旺季提前制定营销策略"


    ]



    insights["actions"]=actions



    print(
        "商业洞察生成完成"
    )



    state["insight"]=insights


    return state