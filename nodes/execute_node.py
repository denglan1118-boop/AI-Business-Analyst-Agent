import sqlite3
import pandas as pd


DB_PATH = r"D:\AI-Projects\AI-Business-Analyst-Agent\database\superstore.db"



def execute_node(state):


    print(
        "\n====== EXECUTE NODE ======"
    )


    sql = state.get(
        "sql"
    )


    if not sql:


        return {

            "raw_data": None,

            "error":
            "SQL为空"

        }



    conn = sqlite3.connect(
        DB_PATH
    )


    try:


        df = pd.read_sql(
            sql,
            conn
        )


    except Exception as e:


        print(
            "SQL执行错误:",
            e
        )


        return {

            "raw_data": None,

            "error":
            str(e)

        }


    finally:


        conn.close()



    print(
        "查询数量:",
        len(df)
    )


    # DataFrame转换成list字典
    data = df.to_dict(
        orient="records"
    )


    return {


        "raw_data":
        data

    }