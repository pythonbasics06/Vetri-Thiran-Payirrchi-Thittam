from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import Base, engine
from .routers import pages, auth, planners, history

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Budget-aware AI recommendation assistant for home, party and jewelry planning.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(history.router)

@app.get("/health", tags=["system"])
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
        "gemini_configured": bool(settings.gemini_api_key.strip()),
        "model": settings.gemini_model,
    }

@app.get("/startup", tags=["system"])
def startup():
    return {"status": "initialized", "service": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
