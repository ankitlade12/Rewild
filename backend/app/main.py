from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes.lookup import router as lookup_router

load_dotenv()

app = FastAPI(
    title="Rewild API",
    description="Consumer ecological scenario engine for micro-habitats",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "rewild-api"}

app.include_router(lookup_router)
