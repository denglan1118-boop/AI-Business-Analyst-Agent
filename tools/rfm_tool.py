import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib
import os

from langchain_core.tools import tool

# 支持中文显示

matplotlib.rcParams["font.sans-serif"] = [
    "SimHei"
]

# 解决负号显示问题

matplotlib.rcParams["axes.unicode_minus"] = False



@tool
def analyze_rfm(data:list):
    """
    客户RFM价值分析

    输入字段:

    Customer ID
    Customer Name
    Last_Date
    Frequency
    Monetary


    输出:

    customer_count
    RFM评分
    客户分层
    Top10客户
    RFM明细
    """

    if isinstance(data, dict):

        rows = data["data"]

    else:

        rows = data


    # =====================
    # 兼容query_database返回格式
    # =====================

    # ======================
    # DataFrame字段处理
    # ======================

    if isinstance(rows[0], dict):

        # SQL返回字典格式
        df = pd.DataFrame(rows)


    else:

        # SQL返回列表格式
        df = pd.DataFrame(

            rows,

            columns=[

                "Customer ID",

                "Customer Name",

                "Last_Date",

                "Frequency",

                "Monetary"

            ]

        )

    # ======================
    # RFM字段校验
    # ======================

    required_columns = [

        "Customer ID",

        "Customer Name",

        "Last_Date",

        "Frequency",

        "Monetary"

    ]

    missing = [

        col

        for col in required_columns

        if col not in df.columns

    ]

    if missing:
        return {

            "analysis_type":

                "RFM客户价值分析",

            "error":

                "输入数据不是RFM数据",

            "missing_columns":

                missing,

            "current_columns":

                df.columns.tolist()

        }

    # 如果SQL没有返回CLV，则Python计算

    # ======================
    # 补充RFM计算字段
    # ======================

    # CLV
    if "CLV" not in df.columns:
        df["CLV"] = (
                df["Monetary"]
                *
                df["Frequency"]
        )

    # Recency
    if "Recency" not in df.columns:
        df["Last_Date"] = pd.to_datetime(
            df["Last_Date"],
            errors="coerce",
            dayfirst=False
        )

        latest_date = df["Last_Date"].max()

        df["Recency"] = (
                latest_date - df["Last_Date"]
        ).dt.days

    # RFM Score
    if "RFM_Score" not in df.columns:
        df["RFM_Score"] = (

                df["Frequency"].rank(
                    pct=True
                )
                +

                df["Monetary"].rank(
                    pct=True
                )

                -

                df["Recency"].rank(
                    pct=True
                )

        )

    print("RFM字段:")
    print(df.columns.tolist())
    # ======================
    # 日期处理兼容
    # ======================

    if "Order Date" in df.columns:

        # 原始订单数据

        df["Order Date"] = pd.to_datetime(
            df["Order Date"]
        )

        analysis_date = (

                df["Order Date"].max()

                +

                pd.Timedelta(days=1)

        )


    elif "Last_Date" in df.columns:

        # SQL已经聚合好的RFM数据

        df["Last_Date"] = pd.to_datetime(
            df["Last_Date"]
        )

        analysis_date = (

                df["Last_Date"].max()

                +

                pd.Timedelta(days=1)

        )


    else:

        raise ValueError(

            f"没有日期字段: {df.columns.tolist()}"

        )

    # =====================
    # RFM分析时间点
    # =====================

    if "Last_Date" in df.columns:

        df["Last_Date"] = pd.to_datetime(
            df["Last_Date"]
        )

        snapshot = df["Last_Date"].max()


    elif "Order Date" in df.columns:

        df["Order Date"] = pd.to_datetime(
            df["Order Date"]
        )

        snapshot = df["Order Date"].max()


    else:

        raise ValueError(
            f"无法找到日期字段:{df.columns.tolist()}"
        )

    # =====================
    # RFM计算
    # =====================

    if "Last_Date" in df.columns:

        print("使用SQL返回的RFM数据")

        rfm = df.copy()

        rfm["Recency"] = (
                snapshot - rfm["Last_Date"]
        ).dt.days


    elif "Order Date" in df.columns:

        print("使用订单明细计算RFM")

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
                    (snapshot - x.max()).days
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

    #==========================
    #RFM字段定义规范
    # ==========================

    # Recency:
    # 距离最近一次购买的天数
    # 数值越小表示客户越活跃

    # Frequency:
    # 客户历史订单数量
    # 只能表示购买次数
    # 禁止使用消费金额推断购买频率

    # Monetary:
    # 客户累计消费金额
    # 只能表示消费价值
    # 禁止使用购买次数替代消费金额

    # R_score:
    # 基于Recency划分的近期活跃评分

    # F_score:
    # 基于Frequency划分的购买频率评分

    # M_score:
    # 基于Monetary划分的消费金额评分

    # 三个维度独立计算，不允许字段互相替代
    # =====================
    # R评分
    # 越近期越高
    # =====================

    rfm["R_score"] = pd.qcut(

        rfm["Recency"].rank(
            method="first"
        ),

        5,

        labels=False

    ) + 1



    # =====================
    # F评分
    # =====================

    rfm["F_score"] = pd.qcut(

        rfm["Frequency"],

        5,

        labels=False,

        duplicates="drop"

    ) + 1



    # =====================
    # M评分
    # =====================

    rfm["M_score"] = pd.qcut(

        rfm["Monetary"].rank(
            method="first"
        ),

        5,

        labels=False

    ) + 1



    # =====================
    # 转整数
    # =====================

    score_columns = [

        "R_score",

        "F_score",

        "M_score"

    ]


    rfm[score_columns] = (

        rfm[score_columns]

        .astype(int)

    )



    # =====================
    # RFM总分
    # =====================

    rfm["RFM_Score"] = (

        rfm["R_score"]

        +

        rfm["F_score"]

        +

        rfm["M_score"]

    )



    # =====================
    # 客户等级
    # =====================

    def customer_level(score):


        if score >= 13:

            return "高价值客户"


        elif score >= 9:

            return "潜力客户"


        else:

            return "普通客户"



    rfm["Customer_Level"] = (

        rfm["RFM_Score"]

        .apply(customer_level)

    )

    # =====================
    # RFM可视化
    # =====================


    # 创建保存目录
    import os

    os.makedirs(
        "visualization",
        exist_ok=True
    )


    # =====================
    # 1. RFM三维散点图
    # =====================


    from mpl_toolkits.mplot3d import Axes3D

    plt.close("all")

    fig = plt.figure(
        figsize=(10, 8),
        dpi=100
    )


    ax = fig.add_subplot(
        111,
        projection="3d"
    )


    levels = (

        rfm["Customer_Level"]

        .unique()

    )


    for lv in levels:


        temp = rfm[

            rfm["Customer_Level"] == lv

        ]


        ax.scatter(

            temp["Recency"],

            temp["Frequency"],

            temp["Monetary"],

            label=lv,

            s=40

        )


    ax.set_xlabel(
        "Recency"
    )

    ax.set_ylabel(
        "Frequency"
    )

    ax.set_zlabel(
        "Monetary"
    )


    ax.set_title(
        "RFM Customer Segmentation"
    )

    ax.legend(
        fontsize=8
    )


    plt.tight_layout()

    # 3D图不要使用tight_layout
    # plt.tight_layout()

    fig.savefig(
        "visualization/rfm_3d_scatter.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    plt.close("all")



    # =====================
    # 2. 客户等级饼图
    # =====================


    level_count = (

        rfm["Customer_Level"]

        .value_counts()

    )

    plt.close("all")

    fig, ax = plt.subplots(
        figsize=(7, 7),
        dpi=100
    )

    ax.pie(
        level_count.values,
        labels=level_count.index,
        autopct="%1.1f%%",
        startangle=90
    )


    plt.title(

        "Customer Level Distribution"

    )

    fig.savefig(
        "visualization/customer_level_pie.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    plt.close("all")
    # =====================
    # 客户生命周期价值 CLV
    # =====================

    rfm["CLV"] = (
            rfm["Monetary"]
            *
            rfm["Frequency"]
    )

    # =====================
    # Top10客户
    # 严格按照Monetary降序
    # =====================

    top10 = (

        rfm.sort_values(
            "Monetary",
            ascending=False
        )

        [
            [
                "Customer ID",
                "Customer Name",
                "Recency",
                "Frequency",
                "Monetary",
                "R_score",
                "F_score",
                "M_score",
                "RFM_Score",
                "CLV"
            ]

        ]

        .head(10)

        .to_dict(
            "records"
        )

    )


    # =====================
    # RFM客户明细
    # 用于Excel / PowerBI
    # =====================

    rfm_detail = (

        rfm

        [

            [

                "Customer ID",

                "Customer Name",

                "Recency",

                "Frequency",

                "Monetary",

                "R_score",

                "F_score",

                "M_score",

                "RFM_Score",

                "Customer_Level",

                "CLV"

            ]

        ]

        .sort_values(

            by="Monetary",

            ascending=False

        )

        .to_dict(

            orient="records"

        )

    )



    # =====================
    # 输出结果
    # =====================

    result = {

        "analysis_date":

            str(snapshot.date()),

        # =====================
        # RFM字段定义说明
        # 防止LLM误解指标含义
        # =====================

        "rfm_definition":

            {

                "Recency":

                    "距离最近一次购买的天数，只代表近期活跃程度",

                "Frequency":

                    "客户历史订单数量，只代表实际购买次数。禁止使用Monetary推断Frequency",

                "Monetary":

                    "客户累计消费金额，只代表消费价值。禁止使用Monetary推断购买频率",

                "R_score":

                    "近期活跃评分，用于衡量客户最近购买活跃程度",

                "F_score":

                    "购买频率评分，用于衡量客户购买次数水平",

                "M_score":

                    "消费金额评分，用于衡量客户消费价值水平"

            },

        "customer_count":

            len(rfm),

        "level_distribution":

            (
                rfm["Customer_Level"]
                .value_counts()
                .to_dict()
            ),

        "average_rfm_score":

            round(

                rfm["RFM_Score"].mean(),

                2

            ),

        "average_monetary":

            round(

                rfm["Monetary"].mean(),

                2

            ),

        "rfm_score_distribution":

            (
                rfm["RFM_Score"]
                .value_counts()
                .sort_index()
                .to_dict()
            ),

        "top10_customer":

            top10,

        "rfm_detail":

            rfm_detail,

        "visualization":

            {

                "rfm_3d_scatter":

                    "visualization/rfm_3d_scatter.png",

                "customer_level_pie":

                    "visualization/customer_level_pie.png"

            }

    }
    return {


        "analysis_type":

        "RFM客户价值分析",



        "summary":

        result

    }