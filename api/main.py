from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from api.agent_api import run_agent
from export.excel_export import generate_excel_report
from api.report_api import create_pdf_report
from fastapi.responses import HTMLResponse

import os



app = FastAPI(

    title="AI Business Analyst Agent",

    version="1.0.0",

    description="基于 LangGraph + LLM + SQL 的智能商业分析Agent"

)



# ==================================================
# 静态资源
# ==================================================

app.mount(

    "/static",

    StaticFiles(

        directory="."

    ),

    name="static"

)



# ==================================================
# 请求模型
# ==================================================

class AnalyzeRequest(BaseModel):

    question:str





# ==================================================
# 首页
# ==================================================

@app.get("/")

def root():

    return {


        "message":

        "AI Business Analyst Agent API running",


        "version":

        "1.0.0"

    }





# ==================================================
# 健康检查
# ==================================================

@app.get("/health")

def health():

    return {


        "status":

        "ok"

    }





# ==================================================
# AI分析接口
# ==================================================

@app.post("/analyze")
def analyze(
    request:AnalyzeRequest
):


    global LAST_RESULT


    result = run_agent(

        request.question

    )


    if result.get(
        "status"
    )=="success":


        LAST_RESULT = result.get(

            "dashboard",

            {}

        )


    return result




# ==================================================
# 单独访问图片
# ==================================================

@app.get("/charts/{filename}")

def charts(filename:str):


    path=os.path.join(

        "charts",

        filename

    )


    if os.path.exists(path):


        return FileResponse(

            path

        )


    return {


        "error":

        "file not found"

    }





# ==================================================
# visualization图片
# ==================================================

@app.get("/visualization/{filename}")

def visualization(filename:str):


    path=os.path.join(

        "visualization",

        filename

    )


    if os.path.exists(path):


        return FileResponse(

            path

        )


    return {


        "error":

        "file not found"

    }

@app.get("/export")
def export_excel():


    if not LAST_RESULT:


        return {


            "error":

            "请先执行/analyze"

        }



    file_path = generate_excel_report(

        LAST_RESULT

    )



    return FileResponse(

        file_path,

        filename="AI_Business_Report.xlsx"

    )



@app.post("/report/pdf")
def generate_pdf(
    request:AnalyzeRequest
):


    pdf_path = create_pdf_report(

        request.question

    )


    return FileResponse(

        pdf_path,

        media_type="application/pdf",

        filename="business_report.pdf"

    )

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard():

    with open(
        "dashboard/index.html",
        encoding="utf-8"
    ) as f:

        return f.read()



from api.excel_report import create_excel_report


@app.get("/report/excel")
def export_excel():


    file = create_excel_report(

        "分析客户价值和销售趋势"

    )


    return FileResponse(

        path=file,

        filename="AI商业分析报告.xlsx",

        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

@app.get("/report/pdf")
def export_pdf():


    file="reports/business_report.pdf"


    return FileResponse(

        path=file,

        filename="AI商业分析报告.pdf",

        media_type="application/pdf"

    )