import streamlit as st
import os
import sys


# ==========================
# 项目路径
# ==========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


if BASE_DIR not in sys.path:

    sys.path.insert(
        0,
        BASE_DIR
    )


# 调用 LangGraph Agent

from run_agent import run_analysis



# ==========================
# 页面配置
# ==========================

st.set_page_config(

    page_title="AI Business Analyst Agent",

    page_icon="🤖",

    layout="wide"

)



# ==========================
# 标题
# ==========================

st.title(
    "🤖 AI Business Analyst Agent"
)


st.markdown(
"""
### 基于 LangGraph + SQL Agent 的智能商业分析系统

功能：

✅ 自动生成SQL  
✅ 数据库查询分析  
✅ RFM客户价值分析  
✅ 客户生命周期价值(CLV)分析  
✅ 销售趋势分析  
✅ 自动生成商业洞察  
✅ 自动生成Markdown / HTML / PDF / Excel报告  

"""
)



# ==========================
# 输入问题
# ==========================

question = st.text_input(

    "请输入分析问题",

    value="分析客户价值和销售趋势"

)



# ==========================
# 开始分析
# ==========================

if st.button(
    "🚀 开始分析"
):


    with st.spinner(
        "AI正在分析数据，请稍候..."
    ):


        try:


            result = run_analysis(
                question
            )


            st.session_state["result"] = result


            st.success(
                "分析完成！"
            )


        except Exception as e:


            st.error(
                f"运行错误：{e}"
            )




# ==========================
# 获取结果
# ==========================

if "result" in st.session_state:


    result = st.session_state["result"]



    # ==========================
    # AI洞察
    # ==========================


    st.divider()


    st.header(
        "🧠 AI商业洞察"
    )


    insight = result.get(
        "insight",
        {}
    )


    if insight:


        st.write(
            insight
        )



    # ==========================
    # 报告展示
    # ==========================


    st.divider()


    st.header(
        "📄 分析报告"
    )


    report = result.get(
        "report",
        ""
    )


    if report:


        st.markdown(
            report
        )




    # ==========================
    # 可视化图片
    # ==========================


    st.divider()


    st.header(
        "📊 可视化分析"
    )


    VIS_DIR = os.path.join(

        BASE_DIR,

        "visualization"

    )



    images = {


        "销售趋势":

        "monthly_sales_trend.png",



        "客户价值分层":

        "customer_segment.png",



        "Top10客户销售贡献":

        "top10_customer_sales.png",



        "产品类别销售贡献":

        "category_sales.png",



        "地区销售表现":

        "region_sales.png",



        "Top10客户消费价值":

        "top10_customer_value.png",



        "Top10客户生命周期价值(CLV)":

        "top10_customer_clv.png"


    }



    cols = st.columns(
        2
    )


    index = 0


    for title, filename in images.items():


        img_path = os.path.join(

            VIS_DIR,

            filename

        )


        if os.path.exists(img_path):


            with cols[index % 2]:


                st.subheader(
                    title
                )


                st.image(

                    img_path,

                    use_container_width=True

                )


            index += 1




    # ==========================
    # 下载报告
    # ==========================


    st.divider()


    st.header(
        "📁 下载文件"
    )


    REPORT_DIR = os.path.join(

        BASE_DIR,

        "reports"

    )


    if os.path.exists(REPORT_DIR):


        files = os.listdir(
            REPORT_DIR
        )


        for file in files:


            file_path = os.path.join(

                REPORT_DIR,

                file

            )


            if os.path.isfile(file_path):


                with open(

                    file_path,

                    "rb"

                ) as f:


                    st.download_button(

                        label=f"下载 {file}",

                        data=f,

                        file_name=file

                    )
