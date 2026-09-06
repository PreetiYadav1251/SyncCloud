
# import os

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, text

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# if DATABASE_URL.startswith("postgresql://"):
#     DATABASE_URL = DATABASE_URL.replace(
#         "postgresql://",
#         "postgresql+psycopg://",
#         1
#     )

# engine = create_engine(DATABASE_URL)

# app = FastAPI(title="SyncCloud API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# engine = create_engine(DATABASE_URL)


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


# @app.get("/database-test")
# def database_test():
#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             value = result.scalar()

#         return {
#             "database": "connected",
#             "test": value
#         }

#     except Exception as e:
#         return {
#             "database": "connection_failed",
#             "error": str(e)
#         }


import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")


# PostgreSQL connection
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# FastAPI application
app = FastAPI(
    title="SyncCloud API",
    description="Cloud-to-cloud file transfer platform",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "app": "SyncCloud",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/database-test")
def database_test():

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            value = result.scalar()

            return {
                "database": "connected",
                "test": value,
            }

    except SQLAlchemyError as e:

        return {
            "database": "connection_failed",
            "error": str(e),
        }