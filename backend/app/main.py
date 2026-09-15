from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from app.routers.auth import router as auth_router
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
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "AssetCare backend is running"}


@app.get("/supabase-test")
def supabase_test():
    return {"message": "Supabase connection is configured"}

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