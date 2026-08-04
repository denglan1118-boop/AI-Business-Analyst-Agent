from tools.analysis_tool import analyze_sales


data = [
    {
        "Sales":100,
        "Profit":20
    },
    {
        "Sales":200,
        "Profit":50
    },
    {
        "Sales":300,
        "Profit":80
    }
]


result = analyze_sales.invoke(
    {
        "data": data
    }
)


print(result)