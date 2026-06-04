from fastapi import FastAPI
from backend.api.routes.search import router as search_router
from backend.api.routes.pdf import router as pdf_router

app = FastAPI(
    title="OpenResearch",
    description="Multi-agent research discovery and analysis platform",
    version="0.1.0"
)

app.include_router(search_router, prefix="/api/v1")
app.include_router(pdf_router, prefix="/api/v1",tags=["PDF"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

