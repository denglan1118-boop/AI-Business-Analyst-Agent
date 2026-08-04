import os
import ast

from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool



# =========================
# 数据库路径
# =========================


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "superstore.db"
)



print("数据库路径:")
print(DB_PATH)




# =========================
# 创建数据库连接
# =========================


db = SQLDatabase.from_uri(
    f"sqlite:///{DB_PATH}",
    sample_rows_in_table_info=0
)




# =========================
# 获取数据库结构
# =========================


@tool
def get_database_schema():
    """
    获取数据库结构。

    生成SQL前必须调用。
    """


    schema = db.get_table_info()



    print(
        "\n数据库schema长度:"
    )

    print(
        len(schema)
    )



    return schema





# =========================
# SQL查询工具
# =========================


@tool
def query_database(sql: str):
    """
    执行SQLite SQL查询。


    数据返回规则:

    1.
    普通查询:
    最大返回100行。


    2.
    RFM客户分析:
    保留完整订单数据。


    3.
    SQL聚合分析:
    正常返回。


    """



    print("\n================")
    print("执行SQL:")
    print(sql)
    print("================")



    try:



        result = db.run(sql)



        print(
            "\n原始结果长度:"
        )

        print(
            len(str(result))
        )




        # =========================
        # LangChain返回字符串转换
        # =========================


        if isinstance(result,str):


            try:


                result = ast.literal_eval(result)



            except:


                pass





        # =========================
        # 数据行限制
        # =========================


        if isinstance(result,list):


            total_rows=len(result)



            print(
                f"\n查询返回行数:{total_rows}"
            )




            # =========================
            # 判断RFM查询
            # =========================


            is_rfm_query=(


                "Customer ID" in sql


                and


                "Customer Name" in sql


                and


                "Order Date" in sql


                and


                "Sales" in sql


                and


                "Customers" in sql


            )





            if is_rfm_query:


                print(
                    "检测到RFM客户分析查询"
                )


                max_rows=None



            else:


                max_rows=100






            # =========================
            # 普通查询限制
            # =========================


            if max_rows is not None:



                if total_rows > max_rows:


                    print(
                        f"⚠️ 数据超过{max_rows}行，仅返回前{max_rows}行"
                    )


                    result=result[:max_rows]



            else:


                print(
                    "RFM分析保留完整数据"
                )







        # =========================
        # 返回结构化结果
        # =========================



        output={



            "row_count":

                len(result)

                if isinstance(result,list)

                else 1,



            "data":

                result



        }




        print(
            "\n最终返回行数:"
        )

        print(
            output["row_count"]
        )



        print(
            "最终返回长度:"
        )


        print(
            len(str(output))
        )



        return output






    except Exception as e:



        error={

            "error":str(e)

        }



        print(
            "\nSQL错误:"
        )

        print(error)



        return error