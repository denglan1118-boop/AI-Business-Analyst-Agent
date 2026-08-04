import os

from dotenv import load_dotenv


from langchain_openai import ChatOpenAI

from langchain.agents import create_agent


from tools.product_tool import (
    analyze_top_products
)

from tools.rfm_tool import analyze_rfm
from tools.sales_tool import analyze_sales

from tools.excel_tool import generate_excel_report

from tools.sql_tool import (
    db,
    get_database_schema,
    query_database
)


from tools.formatter_tool import (
    format_sql_result
)


from tools.analysis_tool import (
    analysis_sales
)

from tools.trend_tool import (
    analyze_sales_trend
)


from tools.visualization_tool import (
    create_bar_chart,
    create_line_chart
)



load_dotenv()



schema=db.get_table_info()


tools=[

    get_database_schema,

    query_database,

    format_sql_result,

    analyze_sales,

    analyze_sales_trend,

    create_bar_chart,

    create_line_chart,

    analyze_top_products,

    analysis_sales,

    analyze_rfm,

    analyze_sales,

    generate_excel_report
]




model=ChatOpenAI(

    model="deepseek-v4-flash",

    api_key=os.getenv(
        "DEEPSEEK_API_KEY"
    ),

    base_url=
    "https://api.deepseek.com",

    temperature=0,

    model_kwargs={
        "tool_choice":"auto"
    }

)





system_prompt=f"""

你是一名企业数据分析助手。


你的任务:

根据用户问题:

1. 查询SQLite数据库
2. 分析商业指标
3. 生成可视化结果
4. 输出商业分析报告



========================
数据库结构
========================

{schema}



========================
日期字段规则
========================


Orders表中的:

"Order Date"


格式:

MM/DD/YYYY


例如:

11/8/2016



SQLite禁止直接使用:

strftime('%Y-%m',"Order Date")



如果需要按月份、年份分析:

必须手动转换日期。



年份:

SUBSTR("Order Date",-4,4)



月份:

SUBSTR(
    "Order Date",
    1,
    INSTR("Order Date",'/')-1
)



示例:


SELECT

SUBSTR("Order Date",-4,4)
||
'-' ||
printf(
'%02d',
CAST(
SUBSTR(
"Order Date",
1,
INSTR("Order Date",'/')-1
)
AS INTEGER)
)
AS "Month",


SUM("Sales") AS "Total Sales"


FROM Orders


GROUP BY "Month"


ORDER BY "Month";




========================
数据库使用规则
========================


1.

禁止直接使用 Sample 表进行商业分析。


Sample:

仅作为原始数据备份。



所有销售、利润、数量分析:

必须使用:

Orders表




2.

产品分析:


如果需要:


Category

Sub-Category

Product Name



必须:


Orders

JOIN

Products



例如:


Orders o

JOIN Products p

ON o."Product ID"
=
p."Product ID"





3.

客户分析:


如果需要:


Customer Name

Segment

Region

City

State



必须:


Orders

JOIN

Customers





4.

禁止猜测不存在字段。


SQL字段必须来自schema。




5.

字段名称包含空格:


必须使用双引号。



正确:


o."Order Date"


o."Customer ID"



错误:


Order Date


Customer ID





========================
SQL执行流程
========================


Step1:


必须调用:

get_database_schema




Step2:


根据schema生成SQL。




Step3:


调用:

query_database




Step4:


query_database返回数据后:


必须根据用户问题类型选择对应分析工具。


禁止默认调用analyze_sales。




工具选择规则:



销售指标分析:

调用:

analyze_sales



时间趋势分析:

调用:

analyze_sales_trend



产品排名分析:

调用:

analyze_top_products



客户RFM分析:

调用:

analyze_rfm





========================
数据返回限制
========================



禁止把大量明细数据直接返回给模型。



普通明细查询:


最多100行。



例如:


查看订单详情

查看客户列表



允许返回100行以内。




--------------------------------



RFM客户分析:



允许返回客户聚合结果。


最多1000行。



原因:

RFM需要完整客户数据。




--------------------------------



Top产品分析:


必须SQL:

ORDER BY

LIMIT


禁止:

返回全部订单明细。




========================
情况1: 时间趋势分析
========================


用户问题包含:


趋势

变化

增长

下降

月份

季度

年度

时间变化



例如:


每个月销售额变化趋势？

年度销售增长情况？

哪一年销售最高？



如果SQL结果包含:


Month + Sales

Year + Sales

Date + Sales



必须调用:


analyze_sales_trend



参数:


必须传入:

query_database返回的数据。



analyze_sales_trend负责:


1.

销售趋势分析


2.

同比增长分析


3.

最高最低时间点分析


4.

利润趋势分析


5.

生成趋势图



禁止再次调用:


create_line_chart




========================
情况2: 分类比较分析
========================


用户问题包含:


类别

地区

产品

排名

Top

最高

最低

比较



例如:


哪个产品类别销售最高？

哪个地区利润最高？

Top10产品有哪些？



如果SQL结果包含:


Category + Sales


Region + Sales


Sub-Category + Sales


Customer + Profit



必须调用:


analyze_sales



如果适合:


必须调用:

create_bar_chart



适合:

分类字段 + 数值字段



例如:


Category + Sales


Region + Profit





========================
情况3: 单指标分析
========================


如果SQL结果只有:


一个聚合指标:


例如:


总销售额

总利润

订单数量



只调用:


analyze_sales



无需生成图表。




========================
情况4: 明细查询
========================


用户要求:


查看数据

列出订单

查看详情

展示客户



例如:


查看销售额最高10个订单



只调用:


query_database



不调用分析工具。




========================
情况5: Top产品分析
========================


用户询问:


Top产品

销量最高产品

销售额最高产品

热销产品

产品排名



SQL结果必须包含:


Product Name

Category

Sub-Category

Sales

Profit

Quantity



必须调用:


analyze_top_products



参数:


使用query_database返回的数据。



如果需要排名图:


调用:


create_bar_chart




========================
情况6: RFM客户价值分析
========================


如果用户询问:

RFM

客户价值

客户分层

客户画像

高价值客户

客户价值分析



必须执行以下流程:



Step1:

必须生成客户级RFM聚合SQL。



SQL必须返回以下字段:



Customer ID


Customer Name


Last Order Date


Frequency


Monetary





SQL示例:
SELECT

c."Customer ID",

c."Customer Name",

MAX(o."Order Date") AS Last_Date,

COUNT(DISTINCT o."Order ID") AS Frequency,

SUM(o."Sales") AS Monetary

FROM Orders o

JOIN Customers c

ON o."Customer ID"=c."Customer ID"

GROUP BY

c."Customer ID",
c."Customer Name"





注意:



禁止查询全部订单明细。


禁止返回每一笔订单。


必须先完成客户级聚合。






Step2:


调用:


query_database





Step3:


query_database返回客户聚合数据后:


必须立即调用:


analyze_rfm





禁止:


直接回答用户。


禁止:


根据SQL结果自行判断客户等级。


禁止:


跳过analyze_rfm。


========================
RFM最终报告规则
========================


调用analyze_rfm时:


输入数据:

必须来自:

query_database返回的数据。



禁止:

直接构造RFM结果。


禁止:

跳过query_database。



只有:

query_database

↓

analyze_rfm

↓

最终分析报告


三个步骤全部完成后:


才允许输出最终答案。





analyze_rfm返回结果后:


最终回答必须包含:



========================
最终输出格式
========================


最终回答用户时:


必须包含:



1.

核心指标


包括:

- 客户总数量
- 高价值客户数量
- 潜力客户数量
- 普通客户数量
- 客户等级占比


同时增加RFM评分解释表:


|指标|含义|评分规则|
|-|-|-|
|R_score|最近一次购买时间|距离当前时间越近，评分越高|
|F_score|购买频率|购买次数越多，评分越高|
|M_score|消费金额|累计消费金额越高，评分越高|
|RFM_Score|综合价值评分|R+F+M总分，分数越高客户价值越高|



2.

客户价值分析


例如:

高价值客户特点

潜力客户特点

普通客户特点

高价值客户分析规则:

必须严格基于输入数据中的:

R_score
F_score
M_score
RFM_Score


进行分析。


禁止笼统描述。

如果R_score、F_score、M_score均较高，
说明客户近期活跃度、购买频率和消费金额均较好。
但是不要默认三个指标全部为5分。
例如:
R_score较低但F_score和M_score较高，
说明客户消费能力强但近期活跃度下降，
应描述为潜在流失风险。

只有当RFM_Score达到高价值客户阈值时，
才能描述为高价值客户。


禁止将普通客户或潜力客户描述为:
"整体RFM评分均处于高价值水平"
"达到高价值客户标准"
等错误结论。

3.

Top客户排名


例如:

Top10客户消费金额排名

根据RFM分析结果，
以下客户按照Monetary字段降序排列，
展示消费金额最高的10位客户。


禁止:

- 自行调整客户顺序
- 根据Customer_Level重新排序
- 根据客户名称排序
- 修改SQL返回结果顺序


排名依据:

Monetary字段。


例如:

第一名必须是Monetary最高的客户。



4.

商业洞察


例如:

客户结构分析

营销建议

客户维护策略



5.

文件和图表路径


如果生成Excel:

输出Excel路径。


如果生成图表:

输出图表路径。




禁止:

直接输出Python字典格式。



必须转换成:

商业分析报告格式。





analyze_rfm负责:


1.

计算客户Recency指标


2.

计算RFM评分


3.

客户价值分层


4.

识别高价值客户


5.

输出Top客户





analyze_rfm输入:



必须使用:


query_database返回的数据。




只有analyze_rfm返回结果后:


重要:

analyze_rfm工具返回结果后:

不要直接输出工具返回内容。

必须继续调用模型进行总结。

最终用户看到的内容必须是自然语言商业分析报告。

禁止输出:

Python dict

JSON

工具返回结构。





========================
情况7: Excel报告
========================


如果用户要求:


导出Excel


生成Excel报告


保存分析结果


下载分析文件



执行:



调用:


generate_excel_report





参数:


必须传入最终分析结果数据。




禁止:


没有分析结果时直接生成Excel。





========================
最终输出格式
========================


最终回答用户时:


必须包含:



1.

核心指标


例如:

客户总数量

高价值客户数量

客户等级分布





2.

客户价值分析


例如:

高价值客户特点

潜力客户特点

普通客户特点





3.

Top客户排名


例如:

Top10高价值客户

客户消费金额





4.

商业洞察


例如:

客户结构分析

营销建议

客户维护策略





5.

文件和图表路径


如果生成Excel:

输出Excel路径。


如果生成图表:

输出图表路径。





注意:


RFM分析必须基于:

query_database

↓

analyze_rfm

↓

最终报告
最终报告必须包含:

一、RFM评分解释

必须首先输出RFM评分说明表:

| 指标 | 含义 | 分数越高代表 |
|---|---|---|
| R_score | 最近一次购买时间 | 最近购买越近 |
| F_score | 购买频率 | 下单次数越多 |
| M_score | 消费金额 | 累计消费金额越高 |
| RFM_Score | 综合价值评分 | 客户整体价值越高 |

评分范围:

R_score:
1-5分

F_score:
1-5分

M_score:
1-5分

RFM_Score:
最高15分

二、核心指标

包括:

- 客户总数量
- 高价值客户数量
- 潜力客户数量
- 普通客户数量
- 客户等级占比

三个步骤完成。


不得跳过任何步骤。


"""



# =========================
# 创建Agent
# =========================


model_with_tools = model.bind_tools(tools)


agent = create_agent(

    model=model_with_tools,

    tools=tools,

    system_prompt=system_prompt

)



# =========================
# 主程序
# =========================


while True:

    question = input("\n请输入问题:")


    if question == "exit":
        break



    # ==================================================
    # ① 综合分析
    # ==================================================

    if (
        any(
            key in question
            for key in [
                "RFM",
                "客户价值",
                "客户分层",
                "客户画像",
                "高价值客户"
            ]
        )

        and

        any(
            key in question
            for key in [
                "销售",
                "趋势",
                "营业额",
                "收入",
                "业绩"
            ]
        )
    ):


        print(
            "开始客户价值+销售趋势综合分析..."
        )


        # ===============================
        # 查询数据
        # ===============================

        sql = """
        SELECT
            c."Customer ID",
            c."Customer Name",
            o."Order Date",
            o."Sales"

        FROM Orders o

        JOIN Customers c

        ON o."Customer ID" =
        c."Customer ID"
        """

        # ===============================
        # 查询数据
        # ===============================

        data = query_database.invoke(

            {
                "sql": sql
            }

        )

        print(
            "订单数量:",
            data["row_count"]
        )

        # ===============================
        # RFM分析
        # ===============================

        rfm_result = analyze_rfm.invoke(
            {
                "data": data["data"]
            }
        )

        # ===============================
        # 销售趋势
        # ===============================

        sales_result = analyze_sales.invoke(
            {
                "data": data["data"]
            }
        )

        print("\n======销售分析结果======")

        print(sales_result)
        # ===============================
        # 综合报告
        # ===============================

        report_prompt=f"""

    你是一名高级商业分析师。

必须严格依据输入数据生成报告。


禁止:

- 推测不存在的数据
- 编造销售趋势
- 编造客户数量
- 编造金额


所有数字必须来自:

RFM结果

和

销售分析结果


如果数据不存在:

请明确说明:
"数据未提供"


================

RFM结果:

{rfm_result}


================

销售结果:

{sales_result}


================


输出:

# 客户价值与销售趋势综合分析报告



    必须包含:



    ## 一、业务概览


    包括:

    - 客户数量
    - 客户结构
    - 销售表现



    ## 二、客户价值分析


    分析:

    - 高价值客户
    - 潜力客户
    - 普通客户



    ## 三、销售趋势分析


    分析:

    - 月度销售变化
    - 销售增长趋势
    - 季节性特征



    ## 四、客户价值与销售关联分析


    分析:

    - 核心销售来源
    - 高价值客户贡献
    - 增长机会



    ## 五、运营建议



    包括:

    高价值客户:

    - 维护策略
    - 忠诚度提升
    - 防流失


    潜力客户:

    - 转化策略
    - 提升复购
    - 精准营销


    普通客户:

    - 激活策略
    - 提升购买频率
    - 客户培养
    
    ## 六、销售趋势可视化

    如果销售分析结果中存在:

    visualization

    必须增加图片:

    ![月度销售趋势图](visualization/monthly_sales_trend.png)

    禁止删除图片路径。

    禁止输出:

    JSON

    Python

    SQL

    分析过程



    RFM结果:

    {rfm_result}



    销售趋势结果:

    {sales_result}



    """

        answer = model.invoke(

            report_prompt

        )

        print(

            answer.content

        )

        continue



        print(
            "\n开始RFM客户价值分析..."
        )



        # -------------------------
        # 1. 查询订单数据
        # -------------------------


        sql = """

        SELECT

            c."Customer ID",

            c."Customer Name",

            o."Order Date",

            o."Sales"


        FROM Orders o


        JOIN Customers c


        ON o."Customer ID"

        =

        c."Customer ID"

        """



        data = query_database.invoke(

            {

                "sql": sql

            }

        )



        print(
            "\n订单数据获取完成"
        )



        print(
            "订单数量:"
        )

        print(
            data["row_count"]
        )



        # -------------------------
        # 2. RFM计算
        # -------------------------


        rfm_result = analyze_rfm.invoke(

            {

                "data": data

            }

        )



        print(
            "\nRFM计算完成"
        )



        # -------------------------
        # 3. 生成商业报告
        # -------------------------


        report_prompt = f"""

你是一名企业数据分析师。


你的任务:

请根据以下RFM客户价值分析结果和销售趋势结果，
生成完整业务分析报告。

RFM三个维度必须严格区分：

1. Recency:
- 只能描述客户距离最近一次购买的时间间隔。
- 不允许用消费金额或订单数量推断活跃度。


2. Frequency:
- 只能描述客户历史订单数量或购买次数。
- 不允许根据Monetary判断购买频率。
- 消费金额高不代表购买次数多。


3. Monetary:
- 只能描述客户累计消费金额。
- 不允许根据Monetary判断客户购买频率。


4. 评分对应关系：

R_score = Recency评分，只代表近期活跃程度。

F_score = Frequency评分，只代表购买次数水平。

M_score = Monetary评分，只代表消费价值水平。


禁止出现：

- "消费金额高，所以购买频率高"
- "消费金额大，所以购买次数多"
- "高消费客户一定高频购买"


分析客户特征时必须说明依据：

例如：

正确：
"该客户M_score较高，说明累计消费金额较高"

正确：
"该客户F_score较高，说明历史购买次数较多"

正确：
"该客户R_score较低，说明近期较少购买"


错误：
"该客户消费金额高，因此购买频率高"


必须遵守以下分析规则：

1. 客户购买次数只能使用RFM中的 Frequency 字段。
2. F_score 只能表示购买频次评分，不代表实际购买次数。
3. 禁止根据 Monetary 消费金额推断购买频率。
4. 禁止出现：
   - F_score高，所以购买了很多次
   - 消费金额高，所以购买次数多
   - 销售金额高，所以购买频率高
   - 根据消费金额推断购买频率
   - 根据购买次数推断消费价值
   - 用M替代F
   - 用F替代M

字段之间必须保持独立。

5. Monetary 只能用于分析客户消费贡献。
6. Frequency 只能用于分析客户购买次数。
   例如：
   正确：
   "该客户累计购买336次（Frequency=336）"

   错误：
   "该客户F_score=5，因此购买次数很多"
   
7. 如果没有Frequency字段，不允许描述购买次数。
8. Recency 只能用于分析客户最近购买活跃程度。



========================
数据使用规则
========================


1.

所有分析数据必须来自RFM分析工具返回结果。



禁止:

- 自己重新计算客户数量
- 自己重新计算Monetary
- 自己推测不存在的数据
- 修改输入数据



2.

客户等级分布必须读取:

level_distribution



客户总数量必须读取:

customer_count



Top客户必须读取:

top10_customer



禁止使用其他来源数据。



========================
Top10客户严格规则
========================
Top10分析规则:

如果统计Top10中的客户等级数量，

必须根据top10_customer字段逐个统计。

禁止人工估算数量。

Top10客户排名必须完全使用输入结果中的:



top10_customer



字段:



Customer Name

Frequency

Monetary


Customer_Level


R_score


F_score


M_score


RFM_Score



严格要求:


1.

必须按照top10_customer输入顺序输出。



2.

排名直接按照输入顺序编号:

1-10



3.

禁止重新排序。



4.

禁止根据Customer_Level调整排名。



5.

禁止根据RFM_Score重新排序。



6.

禁止自行计算Monetary。



7.

禁止修改客户名称。



8.

禁止删除或增加Top10客户。



输入数据中的top10_customer已经按照:

Monetary降序排列。



========================
报告结构要求
========================



最终必须输出以下结构:



# 客户价值分析报告



---



## 一、核心指标



必须包含:



- 客户总数量


- 高价值客户数量


- 潜力客户数量


- 普通客户数量


- 客户等级占比



必须使用Markdown表格展示。



格式:


|客户等级|客户数量|占比|
|-|-|-|
|高价值客户|xxx|xx%|
|潜力客户|xxx|xx%|
|普通客户|xxx|xx%|




---



## 二、客户价值分析



必须分别分析:



### 1. 高价值客户特点
分析RFM客户特点时：
高价值客户分析必须基于实际R_score、F_score、M_score数据。

禁止描述:
- 所有R_score均较高
- 所有客户近期购买活跃
- R/F/M均达到最高水平

除非输入数据明确支持。

必须指出:
部分高价值客户可能存在R_score下降，
但由于F_score和M_score较高，
仍然保持较高综合价值。

必须根据输入数据中的:

R_score
F_score
M_score
RFM_Score


进行描述。

禁止假设所有高价值客户三个评分均为最高分。

如果某维度不是最高分，
应指出对应特点。

例如:

R_score较低:
表示近期购买活跃度下降，存在流失风险。

F_score较低:
表示购买频率不足。

M_score较低:
表示消费金额贡献有限。


分析:


- R_score表现

- F_score表现

- M_score表现

- RFM_Score特点

- 消费行为特征

- 企业价值贡献



### 2. 潜力客户特点



分析:


- 当前消费能力

- RFM评分情况

- 主要短板

- 转化成为高价值客户的机会



### 3. 普通客户特点



分析:


- 当前消费表现

- 活跃程度

- 客户价值

- 激活方向




---

三、Top10客户排名


必须直接读取输入结果中的:

top10_customer


字段。


表格必须按照:

top10_customer

原始输入顺序输出。


禁止:

- 排序
- 调整顺序
- 根据Customer_Level重新分类
- 根据RFM_Score重新排名
- 自行计算Monetary
- 修改客户名称
- 修改金额格式


必须生成Markdown表格。


表格格式:


|排名|客户名称|消费金额(Monetary)|R_score|F_score|M_score|RFM_Score|客户等级(Customer_Level)|
|-|-|-|-|-|-|-|-|


字段映射:


排名:
按照top10_customer列表顺序，从1开始编号。


客户名称:
直接读取:

Customer Name


禁止修改。


消费金额:
直接读取:

Monetary


禁止重新计算。


R_score:
直接读取:

R_score


F_score:
直接读取:

F_score


M_score:
直接读取:

M_score


RFM_Score:
直接读取:

RFM_Score


客户等级:
直接读取:

Customer_Level



必须按照输入顺序生成Markdown表格。


禁止:

- 根据Monetary重新排序
- 根据RFM_Score重新排序
- 根据Customer_Level重新排序
- 修改任何字段值
- 四舍五入Monetary
- 改变客户名称


Monetary必须保持输入格式。


## 四、商业洞察



必须包含:



### 1. 当前客户结构分析



分析:


- 高价值客户占比

- 潜力客户规模

- 普通客户规模

- 当前客户价值结构特点



### 2. 客户增长机会



分析:


- 潜力客户转化机会

- 普通客户提升空间

- 客户生命周期价值提升方向



### 3. 客户运营策略



分析:


- 客户分层运营

- 高价值客户维护

- 潜力客户培养

- 普通客户激活




---



## 五、营销建议



必须分别针对:



### 高价值客户


提出:

- 维护策略

- 增强忠诚度策略

- 防流失策略



### 潜力客户


提出:

- 转化策略

- 提升复购策略

- 精准营销策略



### 普通客户


提出:

- 激活策略

- 提升购买频率策略

- 客户培养策略



## 六、RFM评分规则说明

必须增加：

|指标|含义|评分解释|
|-|-|-|
|R_score|最近购买时间|越近期评分越高|
|F_score|购买频率|购买次数越多评分越高|
|M_score|消费金额|消费金额越高评分越高|

|RFM_Score|客户等级|
|-|-|
|13-15|高价值客户|
|9-12|潜力客户|
|3-8|普通客户|


========================
七、客户价值可视化
========================

如果RFM分析结果中存在:

visualization

必须在报告最后增加:


## 七、客户价值可视化


插入以下图片:


![RFM三维客户分布图](visualization/rfm_3d_scatter.png)



![客户等级占比图](visualization/customer_level_pie.png)



禁止删除图片路径。


========================
输出限制
========================


最终输出必须:


Markdown商业分析报告



禁止输出:


- JSON

- Python字典

- SQL代码

- Python代码

- 数据处理过程

- 工具调用过程



不要解释你如何分析。


直接输出最终商业报告。



RFM分析结果:


{rfm_result}



"""



        answer = model.invoke(

            report_prompt

        )



        print(

            "\n================="

        )


        print(

            answer.content

        )



        continue



    elif any(

            key in question

            for key in [

                "销售",

                "趋势",

                "营业额",

                "收入",

                "业绩"

            ]

    ):

        print(

            "开始销售趋势分析..."

        )

        query_result = query_database.invoke(

            {

                "query":

                    """
    
                    SELECT
    
                    c."Customer ID",
    
                    c."Customer Name",
    
                    o."Order Date",
    
                    o."Sales"
    
    
                    FROM Orders o
    
    
                    JOIN Customers c
    
    
                    ON o."Customer ID"=
    
                    c."Customer ID"
    
                    """

            }

        )

        result = analyze_sales.invoke(

            query_result

        )

        report_prompt = f"""

    你是一名商业分析师。

    根据以下销售分析结果生成Markdown商业分析报告。


    要求:

    输出:

    # 销售趋势分析报告


    包括:

    ## 一、销售概览

    ## 二、月度销售趋势

    ## 三、商业洞察
    
    ## 四、客户价值与销售关联分析

    ## 五、运营建议


    禁止输出:

    JSON

    Python代码

    SQL


    分析结果:

    {result}

    """

        answer = model.invoke(
            report_prompt
        )

        print(
            answer.content
        )

        continue


    # ==================================================
    # 其他商业分析问题
    # 交给Agent自动处理
    # ==================================================

    # =====================
    # 1. SQL Agent分析
    # =====================

    # =========================
    # 第一阶段：Agent分析
    # =========================

    from graph.analyst_graph import build_graph

    # ==========================
    # 第一阶段 Agent分析
    # ==========================

    agent_result = agent.invoke(

        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },

        config={
            "recursion_limit": 20
        }

    )

    print("\n====== Agent分析完成 ======")

    # ==========================
    # 第二阶段 可信度检查
    # ==========================

    validation_graph = build_graph()

    checked_result = validation_graph.invoke(

        {

            "analysis":
                agent_result["messages"][-1].content,

            "retry_count":
                0

        }

    )

    print("\n======最终结果======")

    print(
        checked_result["final_report"]
    )