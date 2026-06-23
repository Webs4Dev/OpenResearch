from fastapi import FastAPI
from backend.api.routes.search import router as search_router
from backend.api.routes.pdf import router as pdf_router
from backend.api.routes.pdf_v2 import router as pdf_v2_router

app = FastAPI(
    title="OpenResearch",
    description="Multi-agent research discovery and analysis platform",
    version="0.1.0"
)

app.include_router(search_router, prefix="/api/v1",tags=["SEARCH"])
app.include_router(pdf_router, prefix="/api/v1",tags=["PDF"])
app.include_router(pdf_v2_router, prefix="/api/v1",tags=["PDF_v2"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

