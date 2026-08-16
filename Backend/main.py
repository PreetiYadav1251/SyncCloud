# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="SyncCloud API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def root():
#     return {
#         "message": "SyncCloud Backend is running"
#     }


# @app.get("/health")
# def health():
#     return {
#         "status": "healthy"
#     }


import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

engine = create_engine(DATABASE_URL)

app = FastAPI(title="SyncCloud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DATABASE_URL)


@app.get("/")
def root():
    return {
        "message": "SyncCloud Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

        return {
            "database": "connected",
            "test": value
        }

    except Exception as e:
        return {
            "database": "connection_failed",
            "error": str(e)
        }