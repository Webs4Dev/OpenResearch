from pydantic import BaseModel


class PDFAnalysisResponse(BaseModel):
    filename:str
    pages:int
    text_length:int
    extracted_text:str