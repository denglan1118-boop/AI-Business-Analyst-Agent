import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

# ==========================
# Power BI Style Theme
# ==========================


plt.rcParams["font.family"] = "Microsoft YaHei"


# 背景

FIG_BG = "#F5F7FA"

CARD_BG = "#FFFFFF"


# Power BI 主色

BI_BLUE = "#118DFF"

BI_GREEN = "#22B573"

BI_ORANGE = "#F2C94C"



# 标题

plt.rcParams["axes.titlesize"] = 16

plt.rcParams["axes.titleweight"] = "bold"



# 去掉边框

plt.rcParams["axes.spines.top"] = False

plt.rcParams["axes.spines.right"] = False


# 网格透明

plt.rcParams["grid.alpha"] = 0.25



def visualization_node(state):


    print(
        "\n====== VISUALIZATION NODE ======"
    )


    analysis = state.get(
        "analysis_result",
        {}
    )


    sales = analysis.get(
        "sales",
        {}
    )

    print("\n====== SALES DEBUG ======")
    print(sales.keys())
    print(sales.get("category_sales"))
    print(sales.get("region_sales"))


    rfm = analysis.get(
        "rfm",
        {}
    )



    # ==========================
    # 图片目录
    # ==========================


    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )


    save_dir = os.path.join(
        BASE_DIR,
        "visualization"
    )


    os.makedirs(
        save_dir,
        exist_ok=True
    )

    for file in os.listdir(save_dir):

        if file.endswith(".png"):
            os.remove(
                os.path.join(
                    save_dir,
                    file
                )
            )

    # ==========================
    # 1. 月销售趋势
    # ==========================

    monthly_sales = sales.get(
        "monthly_sales",
        []
    )

    sales_path = None

    if monthly_sales:

        months = [
            x["Month"]
            for x in monthly_sales
        ]

        values = [
            x["Sales"]
            for x in monthly_sales
        ]

        fig, ax = plt.subplots(
            figsize=(12, 5),
            facecolor=FIG_BG
        )

        ax.set_facecolor(
            CARD_BG
        )

        # 趋势线

        plt.plot(

            months,

            values,

            color=BI_BLUE,

            linewidth=3,

        )

        # 面积填充

        plt.fill_between(

            months,

            values,

            color=BI_BLUE,

            alpha=0.15

        )

        # 平均线

        avg_sales = sum(values) / len(values)

        plt.axhline(
            avg_sales,
            linestyle="--",
            linewidth=1.5,
            label=f"平均销售 {avg_sales / 10000:.1f}万"
        )

        # 最高点

        max_idx = values.index(max(values))

        plt.scatter(
            months[max_idx],
            values[max_idx],
            s=120,
            zorder=5
        )

        plt.annotate(

            f"峰值\n{values[max_idx] / 10000:.1f}万",

            (
                months[max_idx],
                values[max_idx]
            ),

            xytext=(0, 25),

            textcoords="offset points",

            ha="center"

        )

        # 标签减少拥挤

        for i, v in enumerate(values):

            if i % 3 == 0:
                plt.text(
                    i,
                    v,
                    f"{v / 10000:.0f}万",
                    ha="center",
                    fontsize=8
                )

        plt.title(

            "Monthly Sales Trend",

            loc="left",

            fontsize=16,

            fontweight="bold",

            pad=20

        )

        plt.ylabel(
            "Sales"
        )

        plt.gca().yaxis.set_major_formatter(

            ticker.FuncFormatter(
                lambda x, pos:
                f"{x / 10000:.0f}万"
            )

        )

        plt.xticks(
            rotation=45
        )

        plt.grid(
            linestyle="--",
            alpha=0.25
        )

        plt.legend()

        plt.tight_layout()

        plt.savefig(

            os.path.join(
                save_dir,
                "monthly_sales_trend.png"
            ),

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # ==========================
    # 2. 客户分层
    # ==========================

        # ==========================
        # RFM客户价值四象限
        # ==========================

        rfm_df = pd.DataFrame(
            rfm.get(
                "rfm_detail",
                []
            )
        )

        if not rfm_df.empty:

            fig, ax = plt.subplots(

                figsize=(11, 8),

                facecolor=FIG_BG

            )

            ax.set_facecolor(

                CARD_BG

            )

            # ==========================
            # 高价值分界线
            # 使用70%分位数
            # ==========================

            freq_mid = (

                rfm_df["Frequency"]
                .quantile(0.7)

            )

            money_mid = (

                rfm_df["Monetary"]
                .quantile(0.7)

            )

            # ==========================
            # 客户价值分类
            # ==========================

            def classify_customer(row):

                if (

                        row["Frequency"] >= freq_mid

                        and

                        row["Monetary"] >= money_mid

                ):

                    return "核心客户"


                elif (

                        row["Frequency"] < freq_mid

                        and

                        row["Monetary"] >= money_mid

                ):

                    return "潜力客户"


                elif (

                        row["Frequency"] >= freq_mid

                        and

                        row["Monetary"] < money_mid

                ):

                    return "普通客户"


                else:

                    return "流失风险"

            rfm_df["Customer_Type"] = (

                rfm_df.apply(

                    classify_customer,

                    axis=1

                )

            )

            # ==========================
            # 客户颜色
            # ==========================

            color_map = {

                "核心客户":

                    "#E74C3C",

                "潜力客户":

                    "#F39C12",

                "普通客户":

                    "#3498DB",

                "流失风险":

                    "#95A5A6"

            }

            # ==========================
            # 气泡大小
            # 避免大客户遮挡
            # ==========================

            bubble_size = (

                    np.sqrt(

                        rfm_df["Monetary"]

                    )

                    /

                    np.sqrt(

                        rfm_df["Monetary"].max()

                    )

                    *

                    600

            )

            # ==========================
            # 绘制客户散点
            # ==========================

            for category, group in rfm_df.groupby(

                    "Customer_Type"

            ):
                ax.scatter(

                    group["Frequency"],

                    group["Monetary"],

                    s=bubble_size[group.index],

                    alpha=0.65,

                    color=color_map[category],

                    label=(

                        f"{category} "

                        f"({len(group)}人)"

                    ),

                    edgecolors="white",

                    linewidths=0.5

                )

            # ==========================
            # 四象限分割线
            # ==========================

            ax.axvline(

                freq_mid,

                linestyle="--",

                color="#888888",

                linewidth=1.3

            )

            ax.axhline(

                money_mid,

                linestyle="--",

                color="#888888",

                linewidth=1.3

            )

            # ==========================
            # 四象限说明
            # 使用轴比例定位
            # ==========================

            ax.text(

                0.72,

                0.88,

                "⭐ 核心客户\n高频高价值",

                transform=ax.transAxes,

                fontsize=12,

                fontweight="bold"

            )

            ax.text(

                0.08,

                0.88,

                "潜力客户\n高价值低频",

                transform=ax.transAxes,

                fontsize=12

            )

            ax.text(

                0.72,

                0.12,

                "普通客户\n保持运营",

                transform=ax.transAxes,

                fontsize=12

            )

            ax.text(

                0.08,

                0.12,

                "流失风险\n低价值客户",

                transform=ax.transAxes,

                fontsize=12

            )

            # ==========================
            # 坐标轴
            # ==========================

            ax.set_xlabel(

                "Purchase Frequency",

                fontsize=12

            )

            ax.set_ylabel(

                "Customer Value",

                fontsize=12

            )

            ax.set_title(

                "Customer Value Matrix (Frequency-Monetary)",

                loc="left",

                fontsize=17,

                fontweight="bold",

                pad=20

            )

            # ==========================
            # Y轴金额格式
            # ==========================

            ax.yaxis.set_major_formatter(

                ticker.FuncFormatter(

                    lambda x, pos:

                    f"{x / 10000:.0f}万"

                )

            )

            # ==========================
            # 网格
            # ==========================

            ax.grid(

                alpha=0.25

            )

            # ==========================
            # 图例
            # ==========================

            ax.legend(

                title="Customer Segment",

                loc="upper left",

                bbox_to_anchor=(1.02, 1),

                frameon=True

            )

            # ==========================
            # 标注分界值
            # ==========================

            ax.text(

                freq_mid,

                ax.get_ylim()[0],

                f" 频次阈值\n {freq_mid:.0f}",

                fontsize=9,

                color="#666666"

            )

            ax.text(

                ax.get_xlim()[0],

                money_mid,

                f"金额阈值 {money_mid / 10000:.1f}万",

                fontsize=9,

                color="#666666",

                va="bottom"

            )

            plt.tight_layout()

            # ==========================
            # 保存
            # ==========================

            plt.savefig(

                os.path.join(

                    save_dir,

                    "rfm_matrix.png"

                ),

                dpi=300,

                bbox_inches="tight"

            )

            plt.close()

            print(

                "RFM客户价值矩阵生成完成:",

                os.path.join(

                    save_dir,

                    "rfm_matrix.png"

                )

            )

    # ==========================
    # 3. Top10客户销售贡献
    # ==========================

    top_customer = rfm.get(
        "top_customer",
        []
    )

    top_path = None

    if top_customer:

        names = [

            x["Customer Name"]

            for x in top_customer

        ]

        money = [

            x["Monetary"]

            for x in top_customer

        ]

        # ======================
        # 排序
        # ======================

        data = sorted(

            zip(names, money),

            key=lambda x: x[1]

        )

        names = [

            x[0]

            for x in data

        ]

        money = [

            x[1]

            for x in data

        ]

        fig, ax = plt.subplots(
            figsize=(11, 6),
            facecolor=FIG_BG
        )

        ax.set_facecolor(
            CARD_BG
        )

        # ======================
        # 横向柱状图
        # ======================

        bars = plt.barh(

            names,

            money

        )

        # ======================
        # 添加金额标签
        # ======================

        for bar, value in zip(

                bars,

                money

        ):
            plt.text(

                bar.get_width(),

                bar.get_y() + bar.get_height() / 2,

                f"{value / 10000:.1f}万",

                va="center",

                fontsize=10

            )

        # ======================
        # 标题
        # ======================

        plt.title(

            "Top10 Customer Sales Contribution",

            loc="left",

            fontsize=16,

            fontweight="bold",

            pad=20

        )

        plt.xlabel(

            "Sales Amount"

        )

        # ======================
        # 坐标轴优化
        # ======================

        plt.gca().xaxis.set_major_formatter(

            ticker.FuncFormatter(

                lambda x, pos:

                f"{x / 10000:.0f}万"

            )

        )

        plt.grid(

            axis="x",

            linestyle="--",

            alpha=0.3

        )

        plt.tight_layout()

        top_path = os.path.join(

            save_dir,

            "top10_customer_sales.png"

        )

        fig = plt.gcf()

        fig.set_size_inches(
            10,
            6
        )

        plt.savefig(

            top_path,

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

        # ======================
        # 4.Top10客户价值分析图
        # ======================

        top10 = pd.DataFrame(
            rfm.get(
                "top_customer",
                []
            )
        )

        if not top10.empty:

            top10 = (
                top10
                .sort_values(
                    "Monetary",
                    ascending=False
                )
                .head(10)
            )

            fig, ax = plt.subplots(
                figsize=(10, 6),
                facecolor=FIG_BG
            )

            ax.set_facecolor(
                CARD_BG
            )

            # 根据销售金额生成渐变颜色
            norm = plt.Normalize(
                top10["Monetary"].min(),
                top10["Monetary"].max()
            )

            colors = plt.cm.Blues(
                norm(
                    top10["Monetary"]
                )
            )

            bars = plt.bar(

                top10["Customer Name"],

                top10["Monetary"],

                color=colors

            )

            # 添加数值标签
            for bar, value in zip(
                    bars,
                    top10["Monetary"]
            ):
                plt.text(

                    bar.get_x() + bar.get_width() / 2,

                    bar.get_height(),

                    f"{value / 10000:.1f}万",

                    ha="center",

                    va="bottom",

                    fontsize=8

                )

            plt.xticks(

                rotation=45,

                ha="right"

            )

            plt.title(

                "Top10 Customer Monetary Value",

                loc="left",

                fontsize=16,

                fontweight="bold",

                pad=20

            )

            plt.ylabel(
                "Sales"
            )

            plt.gca().yaxis.set_major_formatter(

                ticker.FuncFormatter(

                    lambda x, pos:
                    f"{x / 10000:.0f}万"

                )

            )

            plt.grid(

                axis="y",

                alpha=0.3

            )

            plt.tight_layout()

            plt.savefig(

                os.path.join(

                    save_dir,

                    "top10_customer_value.png"

                ),

                dpi=300,

                bbox_inches="tight"

            )

            plt.close()

        # ======================
        # 5.CLV客户价值排名
        # ======================

        clv_df = pd.DataFrame(

            rfm.get(

                "top_customer",

                []

            )

        )

        print(
            "CLV客户数量:",
            len(clv_df)
        )

        if not clv_df.empty:

            clv_top = (

                clv_df

                .sort_values(

                    "CLV",

                    ascending=False

                )

                .head(10)

            )

            fig, ax = plt.subplots(
                figsize=(10, 6),
                facecolor=FIG_BG
            )

            ax.set_facecolor(
                CARD_BG
            )

            # CLV渐变颜色

            norm = plt.Normalize(

                clv_top["CLV"].min(),

                clv_top["CLV"].max()

            )

            colors = plt.cm.Greens(

                norm(

                    clv_top["CLV"]

                )

            )

            bars = plt.bar(

                clv_top["Customer Name"],

                clv_top["CLV"],

                color=colors

            )

            for bar, value in zip(

                    bars,

                    clv_top["CLV"]

            ):
                plt.text(

                    bar.get_x() + bar.get_width() / 2,

                    bar.get_height(),

                    f"{value / 10000:.1f}万",

                    ha="center",

                    va="bottom",

                    fontsize=8

                )

            plt.xticks(

                rotation=45,

                ha="right"

            )

            plt.title(

                "Top10 Customer CLV",

                loc="left",

                fontsize=16,

                fontweight="bold",

                pad=20

            )

            plt.ylabel(

                "CLV"

            )

            plt.gca().yaxis.set_major_formatter(

                ticker.FuncFormatter(

                    lambda x, pos:
                    f"{x / 10000:.0f}万"

                )

            )

            plt.grid(

                axis="y",

                alpha=0.3

            )

            plt.tight_layout()

            plt.savefig(

                os.path.join(

                    save_dir,

                    "top10_customer_clv.png"

                ),

                dpi=300,

                bbox_inches="tight"

            )

            plt.close()

    # ======================
    # 6. 商品类别销售分析
    # ======================

    category_df = pd.DataFrame(
        sales.get(
            "category_sales",
            []
        )
    )


    print("\n====== CATEGORY DEBUG ======")
    print(category_df)

    # ==========================
    # 类别销售贡献 Donut
    # ==========================

    if not category_df.empty:
        fig, ax = plt.subplots(
            figsize=(8, 8),
            facecolor=FIG_BG
        )

        ax.set_facecolor(
            CARD_BG
        )

        labels = category_df["Category"]

        values = category_df["Sales"]

        wedges, texts, autotexts = plt.pie(

            values,

            labels=labels,

            autopct="%1.1f%%",

            startangle=90,

            pctdistance=0.75,

            wedgeprops={
                "width": 0.35
            }

        )

        total_sales = values.sum()

        plt.text(

            0,

            0,

            f"总销售\n{total_sales / 1000000:.2f}M",

            ha="center",

            va="center",

            fontsize=14,

            fontweight="bold"

        )

        plt.title(

            "Category Sales Contribution",

            loc="left",

            fontsize=16,

            fontweight="bold",

            pad=20

        )

        plt.tight_layout()

        plt.savefig(

            os.path.join(
                save_dir,
                "category_sales.png"
            ),

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # ======================
    # 7.地区销售分析
    # ======================

    region_df = pd.DataFrame(
        sales.get(
            "region_sales",
            []
        )
    )
    print("================")
    print("rfm_df columns:", rfm_df.columns.tolist())
    print("rfm_df shape:", rfm_df.shape)

    print("top10 columns:", top10.columns.tolist())
    print("top10 shape:", top10.shape)

    print("clv columns:", clv_df.columns.tolist())
    print("clv shape:", clv_df.shape)

    print("category columns:", category_df.columns.tolist())
    print("region columns:", region_df.columns.tolist())


    print("\n====== REGION DEBUG ======")
    print(region_df)

    # ==========================
    # 地区销售渐变横向柱状图
    # ==========================

    if not region_df.empty:

        region_df = region_df.sort_values(
            "Sales"
        )

        fig, ax = plt.subplots(
            figsize=(9, 5),
            facecolor=FIG_BG
        )

        ax.set_facecolor(
            CARD_BG
        )

        norm = plt.Normalize(

            region_df["Sales"].min(),

            region_df["Sales"].max()

        )

        colors = plt.cm.Blues(
            norm(
                region_df["Sales"]
            )
        )

        bars = plt.barh(

            region_df["Region"],

            region_df["Sales"],

            color=colors

        )

        for bar, value in zip(
                bars,
                region_df["Sales"]
        ):
            plt.text(

                bar.get_width(),

                bar.get_y()
                +
                bar.get_height() / 2,

                f"{value / 10000:.1f}万",

                va="center",

                fontsize=10

            )

        plt.title(

            "Regional Sales Performance",

            loc="left",

            fontsize=16,

            fontweight="bold",

            pad=20

        )

        plt.xlabel(
            "Sales"
        )

        plt.gca().xaxis.set_major_formatter(

            ticker.FuncFormatter(

                lambda x, pos:
                f"{x / 10000:.0f}万"

            )

        )

        plt.grid(
            axis="x",
            alpha=0.3
        )

        plt.tight_layout()

        plt.savefig(

            os.path.join(
                save_dir,
                "region_sales.png"
            ),

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # ======================
    # KPI Cards
    # ======================

    def create_kpi(
            value,
            title,
            filename
    ):

        fig, ax = plt.subplots(
            figsize=(3, 1.5)
        )

        fig.patch.set_facecolor(
            FIG_BG
        )

        ax.axis("off")

        ax.text(

            0.5,

            0.65,

            value,

            ha="center",

            fontsize=22,

            fontweight="bold",

            color=BI_BLUE

        )

        ax.text(

            0.5,

            0.25,

            title,

            ha="center",

            fontsize=11

        )

        plt.savefig(

            os.path.join(
                save_dir,
                filename
            ),

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    create_kpi(
        "230万",
        "Total Sales",
        "kpi_sales.png"
    )

    create_kpi(
        "793",
        "Customers",
        "kpi_customer.png"
    )

    # ======================
    # 保存可视化结果
    # ======================

    visualization = {}

    image_files = {

        "monthly_sales_trend":
            "monthly_sales_trend.png",

        "rfm_matrix":
            "rfm_matrix.png",

        "top10_customer":
            "top10_customer_sales.png",

        "top10_customer_value":
            "top10_customer_value.png",

        "top10_customer_clv":
            "top10_customer_clv.png",

        "category_sales":
            "category_sales.png",

        "region_sales":
            "region_sales.png"

    }

    for key, filename in image_files.items():

        image_path = os.path.join(
            save_dir,
            filename
        )

        if os.path.exists(image_path):

            visualization[key] = os.path.relpath(
                image_path,
                BASE_DIR
            )

        else:

            visualization[key] = ""

            print(
                f"图片不存在: {image_path}"
            )

    print(
        "可视化路径:",
        visualization
    )

    print(
        "可视化路径:",
        visualization
    )

    return {

        "visualization": visualization

    }