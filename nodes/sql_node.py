def sql_node(state):


    print("\n====== SQL NODE ======")


    question = state.get(
        "question"
    )


    print(
        "用户问题:",
        question
    )



    # =================================
    # 客户价值 + 销售趋势分析
    # =================================

    if (
        "客户" in question
        and
        (
            "销售" in question
            or
            "趋势" in question
        )
    ):


        sql = """

        SELECT

c."Customer ID",
c."Customer Name",

o."Order Date",
o."Sales",

c."Region",

p."Category"


FROM Orders o


JOIN Customers c

ON o."Customer ID" = c."Customer ID"


JOIN Products p

ON o."Product ID" = p."Product ID"

        """



    else:


        # 默认SQL

        sql = """

        SELECT *

        FROM Orders

        LIMIT 100

        """



    print(
        "生成SQL:"
    )

    print(sql)



    return {


        "sql": sql


    }