def report_node(state):


    print(
        "\n====== REPORT NODE ======"
    )


    analysis = state.get(
        "analysis_result",
        {}
    )


    insight = state.get(
        "insight",
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
    # 客户指标
    # =========================


    customer_count = rfm.get(
        "customer_count",
        0
    )


    level_count = rfm.get(
        "level_count",
        {}
    )


    high_value = level_count.get(
        "高价值客户",
        0
    )


    potential = level_count.get(
        "潜力客户",
        0
    )


    normal = level_count.get(
        "普通客户",
        0
    )



    def percent(num):

        if customer_count == 0:

            return "0%"


        return (
            f"{num/customer_count*100:.1f}%"
        )



    # =========================
    # Top10客户
    # =========================

    top_customers = rfm.get(
        "top_customer",
        []
    )

    print("====== TOP客户数据 ======")
    print(top_customers)

    top_table = "\n".join(
        [
            f"|{i}|"
            f"{c['Customer Name']}|"
            f"{c['Monetary']:,.2f}|"
            f"{c['Frequency']}|"
            f"{(c['Monetary'] / c['Frequency'] if c['Frequency'] else 0):,.2f}|"
            f"{c['Recency']}天|"
            f"{c['RFM_Score']}|"
            f"{c['CLV']:,.2f}|"

            for i, c in enumerate(top_customers, 1)
        ]
    )





    total_sales = sales.get(
        "total_sales",
        0
    )

    top_sales = sum(
        c.get("Monetary", 0)
        for c in top_customers
    )

    top10_ratio = (

        top_sales /
        total_sales *
        100

        if total_sales

        else 0

    )

    # =========================
    # Top10平均客单价
    # =========================

    top_frequency = sum(
        c.get("Frequency", 0)
        for c in top_customers
    )

    avg_top_order_value = (

        top_sales /
        top_frequency

        if top_frequency

        else 0

    )



    # =========================
    # 销售指标
    # =========================


    order_count = sales.get(
        "order_count",
        0
    )


    max_month = sales.get(
        "max_month",
        {}
    )


    min_month = sales.get(
        "min_month",
        {}
    )



    monthly_sales = sales.get(
        "monthly_sales",
        []
    )



    avg_month_sales = 0


    sales_growth = 0



    if monthly_sales:


        avg_month_sales = (

            sum(
                x["Sales"]
                for x in monthly_sales
            )

            /

            len(monthly_sales)

        )



        first_sales = monthly_sales[0]["Sales"]

        last_sales = monthly_sales[-1]["Sales"]



        if first_sales != 0:


            sales_growth=(

                (last_sales-first_sales)

                /

                first_sales

                *

                100

            )



    trend="稳定"


    if sales_growth > 0:

        trend="增长"


    elif sales_growth < 0:

        trend="下降"




    # =========================
    # 可视化
    # =========================


    visual = state.get(
        "visualization",
        {}
    )
    print("====== REPORT VISUAL DEBUG ======")

    print(
        state.keys()
    )

    print(
        state.get("visualization")
    )

    monthly_sales_img = visual.get(
        "monthly_sales_trend",
        ""
    ).replace("\\","/")


    customer_segment_img = visual.get(
        "customer_segment",
        ""
    ).replace("\\","/")


    top10_customer_img = visual.get(
        "top10_customer",
        ""
    ).replace("\\","/")

    # ======================
    # 新增商业分析图
    # ======================

    category_sales_img = (
        visual.get(
            "category_sales",
            ""
        )
        .replace("\\", "/")
    )

    region_sales_img = (
        visual.get(
            "region_sales",
            ""
        )
        .replace("\\", "/")
    )

    top10_value_img = (
        visual.get(
            "top10_customer_value",
            ""
        )
        .replace("\\", "/")
    )

    top10_clv_img = (
        visual.get(
            "top10_customer_clv",
            ""
        )
        .replace("\\", "/")
    )

    print(
        "报告图片路径:"
    )

    print(
        category_sales_img,
        region_sales_img,
        top10_value_img,
        top10_clv_img
    )


    # =========================
    # AI洞察
    # =========================


    customer_insight = insight.get(
        "customer",
        ""
    )

    concentration_insight = insight.get(
        "customer_concentration",
        ""
    )

    concentration_insight += (
        f"\n\nTop10客户平均客单价为"
        f"{avg_top_order_value:,.2f}元，"
        "建议重点维护高价值客户，"
        "通过会员体系和精准营销提升客户生命周期价值。"
    )


    sales_insight = insight.get(
        "sales",
        ""
    )


    actions = insight.get(
        "actions",
        []
    )


    action_text = ""


    for a in actions:

        action_text += f"- {a}\n"




    # =========================
    # 商业报告
    # =========================


    report=f"""

# 客户价值与销售趋势商业分析报告


---


# 一、经营概览


## 核心经营指标


|指标|结果|
|-|-|
|客户数量|{customer_count} 人|
|订单数量|{order_count} 单|
|累计销售额|{total_sales:,.2f} 元|
|月均销售额|{avg_month_sales:,.2f} 元|



本次分析基于订单交易数据，

共覆盖：

**{customer_count} 名客户**


累计销售额：

**{total_sales:,.2f} 元**



---


# 二、客户价值分析


## 客户分层情况


|客户类型|数量|占比|
|-|-|-|
|高价值客户|{high_value}|{percent(high_value)}|
|潜力客户|{potential}|{percent(potential)}|
|普通客户|{normal}|{percent(normal)}|



## 客户价值洞察


{customer_insight}



---


# 三、高价值客户分析


## Top10客户


|排名|客户|消费金额|购买次数|平均客单价|最近购买|RFM评分|CLV|
|-|-|-|-|-|-|-|-|
{top_table}



Top10客户累计消费：

**{top_sales:,.2f} 元**


占整体销售：

**{top10_ratio:.2f}%**



{concentration_insight}



---


# 四、销售趋势分析


## 销售表现


|指标|结果|
|-|-|
|最高销售月份|{max_month.get("Month")}|
|最高销售额|{max_month.get("Sales",0):,.2f} 元|
|最低销售月份|{min_month.get("Month")}|
|最低销售额|{min_month.get("Sales",0):,.2f} 元|



## 趋势分析


整体销售趋势：

**{trend}**



首月到末月变化：

**{sales_growth:.2f}%**



月均销售：

**{avg_month_sales:,.2f} 元**



AI销售洞察：

{sales_insight}



---


# 五、商业建议


{action_text}



---


# 六、可视化分析


系统已自动生成以下分析图表：


1. 销售趋势分析

2. 客户价值分层

3. Top10客户销售贡献

4. 产品类别销售贡献

5. 地区销售表现

6. Top10客户消费价值

7. Top10客户生命周期价值（CLV）


详细图表请在系统可视化页面查看。

---


# 七、AI商业洞察总结


## 客户洞察

{customer_insight}



## 客户集中度分析

{concentration_insight}



## 销售趋势分析

{sales_insight}



---


# 八、总结


1. 客户结构存在明显价值分层，
高价值客户是核心收入贡献群体。


2. 潜力客户规模较大，
具备进一步增长空间。


3. 销售呈现周期变化，
企业应结合历史数据制定经营策略。


"""


    return {

        "report":
        report

    }