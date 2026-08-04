import pandas as pd



def analysis_node(state):


    print("==========进入 analysis_node==========")


    raw_data = state.get(
        "raw_data"
    )

    print("raw_data类型:", type(raw_data))

    print(
        "raw_data前两条:",
        raw_data[:2] if isinstance(raw_data, list) else raw_data
    )


    if raw_data is None:

        return {

            "error":
            "没有分析数据"

        }



    # ======================
    # DataFrame处理
    # ======================

    if isinstance(
        raw_data,
        pd.DataFrame
    ):

        df = raw_data.copy()

    else:

        df = pd.DataFrame(raw_data)

    print("转换后的字段:")
    print(df.columns.tolist())

    required_columns = [
        "Customer ID",
        "Customer Name",
        "Order Date",
        "Sales"
    ]

    missing_columns = [

        col

        for col in required_columns

        if col not in df.columns

    ]

    if missing_columns:
        return {

            "error":

                f"缺少字段: {missing_columns}",

            "columns":

                df.columns.tolist()

        }

    print(
        "开始客户价值+销售趋势分析"
    )
    print("当前df字段:")
    print(df.columns.tolist())

    print("当前df维度:")
    print(df.shape)


    # ======================
    # 日期处理
    # ======================

    # ======================
    # 判断数据类型
    # ======================

    # ======================
    # 日期字段处理
    # ======================

    print(
        "分析字段:",
        df.columns.tolist()
    )

    # ======================
    # SQL已经计算好的RFM结果
    # ======================

    if "Last_Order_Date" in df.columns:

        print(
            "检测到RFM SQL结果"
        )

        rfm = df.copy()

        rfm["Last_Order_Date"] = pd.to_datetime(

            rfm["Last_Order_Date"]

        )

        analysis_date = (

                rfm["Last_Order_Date"].max()

                +

                pd.Timedelta(days=1)

        )

        rfm["Recency"] = (

                analysis_date

                -

                rfm["Last_Order_Date"]

        ).dt.days



    # ======================
    # 原始订单明细
    # ======================

    elif "Order Date" in df.columns:

        print(
            "检测到订单明细，重新计算RFM"
        )

        df["Last_Date"] = pd.to_datetime(
            df["Last_Date"]
        )

        analysis_date = (

                df["Order Date"].max()

                +

                pd.Timedelta(days=1)

        )

        rfm = (

            df.groupby(

                [
                    "Customer ID",
                    "Customer Name"
                ]

            )

            .agg(

                Recency=(

                    "Order Date",

                    lambda x:

                    (
                            analysis_date - x.max()
                    ).days

                ),

                Frequency=(

                    "Order Date",

                    "count"

                ),

                Monetary=(

                    "Sales",

                    "sum"

                )

            )

            .reset_index()

        )


    else:

        return {

            "error":

                "没有找到日期字段",

            "columns":

                df.columns.tolist()

        }

    # ======================
    # RFM分析
    # ======================


    rfm = (

        df.groupby(
            [
                "Customer ID",
                "Customer Name"
            ]
        )

        .agg(

            Recency=(

                "Order Date",

                lambda x:
                (
                    analysis_date-x.max()
                ).days

            ),


            Frequency=(

                "Order Date",

                "count"

            ),


            Monetary=(

                "Sales",

                "sum"

            )

        )

        .reset_index()

    )



    rfm["R_score"] = pd.qcut(

        rfm["Recency"],

        5,

        labels=[5,4,3,2,1],

        duplicates="drop"

    )



    rfm["F_score"] = pd.qcut(

        rfm["Frequency"],

        5,

        labels=[1,2,3,4,5],

        duplicates="drop"

    )


    rfm["M_score"] = pd.qcut(

        rfm["Monetary"],

        5,

        labels=[1,2,3,4,5],

        duplicates="drop"

    )



    for col in [
        "R_score",
        "F_score",
        "M_score"
    ]:

        rfm[col] = (
            rfm[col]
            .astype(int)
        )

    def customer_type(x):

        if x >= 12:

            return "核心客户"


        elif x >= 9:

            return "潜力客户"


        elif x >= 6:

            return "普通客户"


        else:

            return "流失风险"

    def customer_type(x):

        if x >= 12:

            return "高价值客户"

        elif x >= 8:

            return "潜力客户"

        else:

            return "普通客户"

    rfm["Customer_Level"] = (

        rfm["RFM_Score"]

        .apply(customer_type)

    )

    # 客户生命周期价值
    rfm["CLV"] = rfm["Monetary"]

    rfm_result = {

        "customer_count":

            len(rfm),

        "level_count":

            rfm["Customer_Level"]
            .value_counts()
            .to_dict(),

        # ======================
        # RFM客户明细（Excel使用）
        # ======================

        "rfm_detail":

            rfm[
                [
                    "Customer ID",
                    "Customer Name",
                    "Recency",
                    "Last_Order_Date",
                    "Frequency",
                    "Monetary",
                    "RFM_Score",
                    "Customer_Level",
                    "CLV",
                    "R_score",
                    "F_score",
                    "M_score",
                ]
            ]

            .sort_values(
                "Monetary",
                ascending=False
            )

            .to_dict(
                "records"
            ),

        # ======================
        # Top10客户
        # ======================

        "top_customer":

            rfm.sort_values(
                "Monetary",
                ascending=False
            )
            [
                [
                    "Customer Name",
                    "Monetary",
                    "Frequency",
                    "Recency",
                    "RFM_Score",
                    "CLV",
                    "R_score",
                    "F_score",
                    "M_score",
                ]
            ]

            .head(10)

            .assign(

                Avg_Order_Value=lambda x:
                x["Monetary"] / x["Frequency"]

            )

            .to_dict(
                "records"
            )

    }

    # ======================
    # 销售趋势
    # ======================


    df["Month"] = (

        df["Order Date"]

        .dt

        .to_period("M")

        .astype(str)

    )


    monthly_sales=(

        df.groupby(
            "Month"
        )
        ["Sales"]

        .sum()

        .reset_index()

    )

    # ======================
    # 商品类别销售分析
    # ======================

    category_sales = (

        df.groupby(
            "Category"
        )
        ["Sales"]

        .sum()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )

    # ======================
    # 地区销售分析
    # ======================

    region_sales = (

        df.groupby(
            "Region"
        )
        ["Sales"]

        .sum()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )

    sales_result={


        "total_sales":

        float(
            df["Sales"].sum()
        ),



        "order_count":

        len(df),



        "max_month":

        monthly_sales.loc[

            monthly_sales["Total Sales"]
            .idxmax()

        ]

        .to_dict(),



        "min_month":

        monthly_sales.loc[

            monthly_sales["Total Sales"]
            .idxmin()

        ]

        .to_dict(),



        "monthly_sales":

        monthly_sales.to_dict(
            "records"
        )

    }

    # ======================
    # 整理分析结果
    # ======================

    customer_analysis = {

        "customer_count":

            len(rfm),

        "top10_sales":

            float(

                rfm.sort_values(
                    "Monetary",
                    ascending=False
                )
                .head(10)
                ["Monetary"]
                .sum()

            ),

        "avg_customer_value":

            float(

                rfm["Monetary"]
                .mean()

            )

    }

    sales_trend = {

        "monthly_sales":

            monthly_sales.to_dict(
                "records"
            ),

        "best_month":

            monthly_sales.loc[

                monthly_sales["Total Sales"]
                .idxmax()

            ]
            .to_dict(),

        "worst_month":

            monthly_sales.loc[

                monthly_sales["Total Sales"]
                .idxmin()

            ]
            .to_dict()

    }

    # ======================
    # 写入State
    # ======================

    state["rfm"] = rfm_result

    state["sales"] = {

        **sales_result,

        "category_sales":

            category_sales.to_dict(
                "records"
            ),

        "region_sales":

            region_sales.to_dict(
                "records"
            )

    }

    state["sales_trend"] = sales_trend

    state["customer_analysis"] = customer_analysis

    # 保留原来的
    state["analysis_result"] = {

        "rfm":

            state["rfm"],

        "sales":

            state["sales"]

    }

    print(
        "分析完成"
    )

    return state