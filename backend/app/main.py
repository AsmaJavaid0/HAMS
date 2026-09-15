import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from supabase import Client, create_client
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    Client = None
    create_client = None

from app.routers import (
    assets,
    audit,
    compliance,
    departments,
    documents,
    locations,
    maintenance,
    movements,
    notifications,
)
from app.routers.auth import router as auth_router

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")

if SUPABASE_URL and SUPABASE_KEY and create_client is not None:
    supabase: Client | None = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AssetCare backend is running"}


@app.get("/supabase-test")
def supabase_test():
    if supabase is None:
        return {
            "message": "Supabase is not configured in this environment.",
            "configured": False,
        }

    return {
        "message": "Supabase connection is configured",
        "configured": True,
    }

app.include_router(auth_router)
app.include_router(departments.router)
app.include_router(locations.router)
app.include_router(assets.router)
app.include_router(maintenance.router)
app.include_router(compliance.router)
app.include_router(documents.router)
app.include_router(movements.router)
app.include_router(notifications.router)
app.include_router(audit.router)
