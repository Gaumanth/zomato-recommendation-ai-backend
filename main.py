import sys
import os
from contextlib import asynccontextmanager

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from data.data_loader import get_dataframe


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading Zomato dataset on startup...")
    try:
        df = get_dataframe()
        print(f"Dataset loaded: {len(df)} restaurants")
    except Exception as e:
        print(f"Warning: Could not pre-load dataset: {e}")
    yield


app = FastAPI(
    title="Zomato AI Restaurant Recommendation Service",
    description="Get personalized restaurant recommendations powered by Gemini AI",
    version="1.0.0",
    lifespan=lifespan,
)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
