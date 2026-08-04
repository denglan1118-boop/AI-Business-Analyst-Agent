def correction_node(state):


    print(
        "\n====== CORRECTION NODE ======"
    )


    retry = state.get(
        "retry_count",
        0
    )


    error = state.get(
        "error"
    )


    print(
        "错误:",
        error
    )


    retry += 1



    # 最大重试3次

    if retry >= 3:

        return {

            "retry_count": retry,

            "validation":
            "failed",

            "error":
            "SQL连续失败3次"

        }



    # 这里以后接LLM自动修SQL

    old_sql = state.get(
        "sql",
        ""
    )


    new_sql = old_sql



    return {


        "retry_count":
        retry,


        "sql":
        new_sql,


        "error":
        None

    }