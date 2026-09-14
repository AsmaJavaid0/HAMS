from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from app.routers.auth import router as auth_router
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