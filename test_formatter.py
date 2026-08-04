from tools.formatter_tool import format_sql_result


data=[
    ("Technology",893633.28),
    ("Furniture",764284.65)
]


print(
    format_sql_result.invoke(
        {
            "rows":data
        }
    )
)