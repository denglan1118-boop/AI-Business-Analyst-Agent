def validation_node(state):


    sql = state.get(
        "sql"
    )


    raw_data = state.get(
        "raw_data"
    )


    print(
        "\n====== VALIDATION NODE ======"
    )


    print(
        "SQL:",
        sql
    )

    print(
        "数据量:",
        len(raw_data) if raw_data is not None else 0
    )



    # =====================
    # 1. SQL检查
    # =====================

    if not sql:


        return {

            "validation":
            "failed",

            "error":
            "SQL为空"

        }



    # =====================
    # 2. 数据检查
    # =====================

    if raw_data is None:


        return {

            "validation":
            "failed",

            "error":
            "没有查询结果"

        }



    # =====================
    # 3. 空结果检查
    # =====================

    if len(raw_data)==0:


        return {

            "validation":
            "failed",

            "error":
            "查询结果为空"

        }



    # =====================
    # 通过
    # =====================

    print(
        "SQL验证通过"
    )


    return {


        "validation":
        "pass",


        "error":
        None

    }