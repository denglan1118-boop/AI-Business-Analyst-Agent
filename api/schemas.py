from pydantic import BaseModel


class AnalysisRequest(BaseModel):

    question: str