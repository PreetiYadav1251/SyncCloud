# import os

# from dotenv import load_dotenv
# from fastapi import FastAPI
# from sqlalchemy import create_engine, text
# from sqlalchemy.exc import SQLAlchemyError


# # Load environment variables
# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise RuntimeError("DATABASE_URL is not set in .env")


# # PostgreSQL connection
# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
# )


# # FastAPI application
# app = FastAPI(
#     title="SyncCloud API",
#     description="Cloud-to-cloud file transfer platform",
#     version="1.0.0",
# )


# @app.get("/")
# def root():
#     return {
#         "app": "SyncCloud",
#         "status": "running",
#     }


# @app.get("/health")
# def health():
#     return {
#         "status": "healthy",
#     }


# @app.get("/database-test")
# def database_test():

#     try:
#         with engine.connect() as connection:

#             result = connection.execute(
#                 text("SELECT 1")
#             )

#             value = result.scalar()

#             return {
#                 "database": "connected",
#                 "test": value,
#             }

#     except SQLAlchemyError as e:

#         return {
#             "database": "connection_failed",
#             "error": str(e),
#         }


# import os
# import secrets
# from urllib.parse import urlencode

# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException, Request
# from fastapi.responses import RedirectResponse, JSONResponse
# from sqlalchemy import create_engine, text
# from sqlalchemy.exc import SQLAlchemyError
# from starlette.middleware.sessions import SessionMiddleware
# import httpx


# # =========================================================
# # LOAD ENVIRONMENT VARIABLES
# # =========================================================

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# GOOGLE_REDIRECT_URI = os.getenv(
#     "GOOGLE_REDIRECT_URI",
#     "http://localhost:8000/auth/google/callback",
# )

# SESSION_SECRET = os.getenv("SESSION_SECRET")

# if not DATABASE_URL:
#     raise RuntimeError("DATABASE_URL is not set in .env")

# if not GOOGLE_CLIENT_ID:
#     raise RuntimeError("GOOGLE_CLIENT_ID is not set in .env")

# if not GOOGLE_CLIENT_SECRET:
#     raise RuntimeError("GOOGLE_CLIENT_SECRET is not set in .env")

# if not SESSION_SECRET:
#     raise RuntimeError("SESSION_SECRET is not set in .env")


# # =========================================================
# # DATABASE
# # =========================================================

# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
# )


# # =========================================================
# # FASTAPI APPLICATION
# # =========================================================

# app = FastAPI(
#     title="SyncCloud API",
#     description="Cloud-to-cloud file transfer platform",
#     version="1.0.0",
# )


# # =========================================================
# # SESSION MIDDLEWARE
# # =========================================================

# app.add_middleware(
#     SessionMiddleware,
#     secret_key=SESSION_SECRET,
#     same_site="lax",
#     https_only=False,
# )


# # =========================================================
# # GOOGLE OAUTH CONFIGURATION
# # =========================================================

# GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

# GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

# GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# GOOGLE_DRIVE_SCOPE = (
#     "https://www.googleapis.com/auth/drive"
# )


# # =========================================================
# # BASIC ROUTES
# # =========================================================

# @app.get("/")
# def root():
#     return {
#         "app": "SyncCloud",
#         "status": "running",
#     }


# @app.get("/health")
# def health():
#     return {
#         "status": "healthy",
#     }


# # =========================================================
# # DATABASE TEST
# # =========================================================

# @app.get("/database-test")
# def database_test():

#     try:

#         with engine.connect() as connection:

#             result = connection.execute(
#                 text("SELECT 1")
#             )

#             value = result.scalar()

#             return {
#                 "database": "connected",
#                 "test": value,
#             }

#     except SQLAlchemyError as e:

#         return {
#             "database": "connection_failed",
#             "error": str(e),
#         }


# # =========================================================
# # GOOGLE LOGIN
# # =========================================================

# @app.get("/auth/google/login")
# def google_login(request: Request):

#     # Generate CSRF protection state
#     state = secrets.token_urlsafe(32)

#     request.session["google_oauth_state"] = state

#     params = {
#         "client_id": GOOGLE_CLIENT_ID,
#         "redirect_uri": GOOGLE_REDIRECT_URI,
#         "response_type": "code",
#         "scope": GOOGLE_DRIVE_SCOPE,
#         "access_type": "offline",
#         "prompt": "consent",
#         "state": state,
#     }

#     google_url = (
#         GOOGLE_AUTH_URL
#         + "?"
#         + urlencode(params)
#     )

#     return RedirectResponse(
#         url=google_url
#     )


# # =========================================================
# # GOOGLE CALLBACK
# # =========================================================

# @app.get("/auth/google/callback")
# async def google_callback(
#     request: Request,
#     code: str | None = None,
#     state: str | None = None,
#     error: str | None = None,
# ):

#     # User cancelled authorization
#     if error:
#         return JSONResponse(
#             {
#                 "success": False,
#                 "error": error,
#             },
#             status_code=400,
#         )

#     # Missing authorization code
#     if not code:
#         raise HTTPException(
#             status_code=400,
#             detail="Google authorization code missing",
#         )

#     # Verify OAuth state
#     saved_state = request.session.get(
#         "google_oauth_state"
#     )

#     if not state or state != saved_state:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid OAuth state",
#         )

#     # Remove state after successful verification
#     request.session.pop(
#         "google_oauth_state",
#         None,
#     )

#     # =====================================================
#     # EXCHANGE CODE FOR TOKENS
#     # =====================================================

#     token_data = {
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "code": code,
#         "grant_type": "authorization_code",
#         "redirect_uri": GOOGLE_REDIRECT_URI,
#     }

#     async with httpx.AsyncClient() as client:

#         token_response = await client.post(
#             GOOGLE_TOKEN_URL,
#             data=token_data,
#         )

#     if token_response.status_code != 200:

#         return JSONResponse(
#             {
#                 "success": False,
#                 "error": "Failed to obtain Google access token",
#                 "details": token_response.text,
#             },
#             status_code=400,
#         )

#     tokens = token_response.json()

#     access_token = tokens.get(
#         "access_token"
#     )

#     refresh_token = tokens.get(
#         "refresh_token"
#     )

#     token_type = tokens.get(
#         "token_type",
#         "Bearer",
#     )

#     expires_in = tokens.get(
#         "expires_in"
#     )

#     scope = tokens.get(
#         "scope"
#     )

#     # =====================================================
#     # GET GOOGLE ACCOUNT INFORMATION
#     # =====================================================

#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }

#     async with httpx.AsyncClient() as client:

#         user_response = await client.get(
#             GOOGLE_USERINFO_URL,
#             headers=headers,
#         )

#     if user_response.status_code != 200:

#         return JSONResponse(
#             {
#                 "success": False,
#                 "error": "Unable to retrieve Google account",
#                 "details": user_response.text,
#             },
#             status_code=400,
#         )

#     google_user = user_response.json()

#     google_email = google_user.get(
#         "email"
#     )

#     google_name = google_user.get(
#         "name"
#     )

#     google_id = google_user.get(
#         "id"
#     )

#     # =====================================================
#     # TEMPORARY RESPONSE
#     # =====================================================

#     # For now we return the account information.
#     #
#     # In the next step we will:
#     #
#     # 1. Create/find the SyncCloud user
#     # 2. Create cloud_accounts row
#     # 3. Encrypt the tokens
#     # 4. Store them in oauth_tokens
#     # 5. Fetch Google Drive files
#     #
#     # Do NOT expose tokens in production responses.

#     return {
#         "success": True,
#         "provider": "google_drive",
#         "account": {
#             "google_id": google_id,
#             "email": google_email,
#             "name": google_name,
#         },
#         "token_received": bool(access_token),
#         "refresh_token_received": bool(refresh_token),
#         "expires_in": expires_in,
#         "scope": scope,
#         "token_type": token_type,
#         "message": "Google Drive connected successfully",
#     }


import os
import secrets
from datetime import datetime, timezone
from urllib.parse import urlencode
from uuid import uuid4

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI",
    "http://localhost:8000/auth/google/callback"
)


# ============================================================
# VALIDATE ENVIRONMENT
# ============================================================

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

if not GOOGLE_CLIENT_ID:
    raise RuntimeError("GOOGLE_CLIENT_ID is not set in .env")

if not GOOGLE_CLIENT_SECRET:
    raise RuntimeError("GOOGLE_CLIENT_SECRET is not set in .env")


# ============================================================
# DATABASE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="SyncCloud API",
    description="Cloud-to-cloud file transfer platform",
    version="1.0.0",
)


# ============================================================
# GOOGLE OAUTH SETTINGS
# ============================================================

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

GOOGLE_DRIVE_URL = "https://www.googleapis.com/drive/v3/files"


# We need Drive access for SyncCloud.
GOOGLE_SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/drive",
]


# Temporary state storage for local development.
#
# In production this should be stored in a proper session/cache
# such as Redis or a database.
oauth_states = {}


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "app": "SyncCloud",
        "status": "running",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# ============================================================
# DATABASE TEST
# ============================================================

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


# ============================================================
# GOOGLE LOGIN
# ============================================================

@app.get("/auth/google/login")
def google_login():

    # Generate CSRF protection state
    state = secrets.token_urlsafe(32)

    oauth_states[state] = {
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }

    google_url = (
        f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    )

    return RedirectResponse(
        url=google_url
    )


# ============================================================
# GOOGLE CALLBACK
# ============================================================

@app.get("/auth/google/callback")
def google_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
):

    # --------------------------------------------------------
    # GOOGLE RETURNED AN ERROR
    # --------------------------------------------------------

    if error:

        return {
            "success": False,
            "error": "Google authorization failed",
            "details": error,
        }


    # --------------------------------------------------------
    # CHECK CODE
    # --------------------------------------------------------

    if not code:

        raise HTTPException(
            status_code=400,
            detail="Authorization code was not provided by Google."
        )


    # --------------------------------------------------------
    # CHECK STATE
    # --------------------------------------------------------

    if not state:

        raise HTTPException(
            status_code=400,
            detail="OAuth state was not provided."
        )


    if state not in oauth_states:

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state."
        )


    # State has now been used.
    del oauth_states[state]


    # --------------------------------------------------------
    # EXCHANGE AUTHORIZATION CODE FOR TOKENS
    # --------------------------------------------------------

    token_payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }


    try:

        token_response = requests.post(
            GOOGLE_TOKEN_URL,
            data=token_payload,
            timeout=30,
        )

    except requests.RequestException as e:

        return {
            "success": False,
            "error": "Unable to connect to Google token service",
            "details": str(e),
        }


    if not token_response.ok:

        return {
            "success": False,
            "error": "Unable to exchange Google authorization code",
            "details": token_response.text,
        }


    token_data = token_response.json()


    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    token_type = token_data.get("token_type", "Bearer")
    expires_in = token_data.get("expires_in")
    scope = token_data.get("scope")


    if not access_token:

        return {
            "success": False,
            "error": "Google did not return an access token",
            "details": token_data,
        }


    # --------------------------------------------------------
    # CALCULATE TOKEN EXPIRATION
    # --------------------------------------------------------

    expires_at = None

    if expires_in:

        try:

            expires_at = datetime.now(timezone.utc).replace(
                microsecond=0
            )

            from datetime import timedelta

            expires_at = expires_at + timedelta(
                seconds=int(expires_in)
            )

        except Exception:

            expires_at = None


    # --------------------------------------------------------
    # GET GOOGLE ACCOUNT INFORMATION
    #
    # IMPORTANT:
    # We MUST send the access token here.
    # This fixes your current 401 error.
    # --------------------------------------------------------

    try:

        userinfo_response = requests.get(
            GOOGLE_USERINFO_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=30,
        )

    except requests.RequestException as e:

        return {
            "success": False,
            "error": "Unable to retrieve Google account",
            "details": str(e),
        }


    if not userinfo_response.ok:

        return {
            "success": False,
            "error": "Unable to retrieve Google account",
            "details": userinfo_response.text,
        }


    google_user = userinfo_response.json()


    google_id = google_user.get("id")
    google_email = google_user.get("email")
    google_name = google_user.get("name")


    if not google_email:

        return {
            "success": False,
            "error": "Google account email was not returned",
            "details": google_user,
        }


    # --------------------------------------------------------
    # SAVE USER IN DATABASE
    # --------------------------------------------------------

    try:

        with engine.begin() as connection:

            # Look for existing user
            existing_user = connection.execute(
                text("""
                    SELECT id
                    FROM users
                    WHERE email = :email
                    LIMIT 1
                """),
                {
                    "email": google_email
                }
            ).fetchone()


            if existing_user:

                user_id = existing_user[0]

                connection.execute(
                    text("""
                        UPDATE users
                        SET
                            name = :name,
                            updated_at = NOW()
                        WHERE id = :user_id
                    """),
                    {
                        "name": google_name,
                        "user_id": user_id,
                    }
                )

            else:

                user_id = uuid4()

                connection.execute(
                    text("""
                        INSERT INTO users (
                            id,
                            name,
                            email,
                            created_at,
                            updated_at
                        )
                        VALUES (
                            :id,
                            :name,
                            :email,
                            NOW(),
                            NOW()
                        )
                    """),
                    {
                        "id": user_id,
                        "name": google_name,
                        "email": google_email,
                    }
                )


            # ------------------------------------------------
            # SAVE GOOGLE CLOUD ACCOUNT
            # ------------------------------------------------

            existing_account = connection.execute(
                text("""
                    SELECT id
                    FROM cloud_accounts
                    WHERE
                        user_id = :user_id
                        AND provider = :provider
                        AND account_email = :account_email
                    LIMIT 1
                """),
                {
                    "user_id": user_id,
                    "provider": "google_drive",
                    "account_email": google_email,
                }
            ).fetchone()


            if existing_account:

                cloud_account_id = existing_account[0]

                connection.execute(
                    text("""
                        UPDATE cloud_accounts
                        SET
                            account_name = :account_name,
                            is_active = TRUE,
                            updated_at = NOW()
                        WHERE id = :id
                    """),
                    {
                        "account_name": google_name,
                        "id": cloud_account_id,
                    }
                )

            else:

                cloud_account_id = uuid4()

                connection.execute(
                    text("""
                        INSERT INTO cloud_accounts (
                            id,
                            user_id,
                            provider,
                            account_email,
                            account_name,
                            is_active,
                            created_at,
                            updated_at
                        )
                        VALUES (
                            :id,
                            :user_id,
                            :provider,
                            :account_email,
                            :account_name,
                            TRUE,
                            NOW(),
                            NOW()
                        )
                    """),
                    {
                        "id": cloud_account_id,
                        "user_id": user_id,
                        "provider": "google_drive",
                        "account_email": google_email,
                        "account_name": google_name,
                    }
                )


            # ------------------------------------------------
            # SAVE OAUTH TOKENS
            # ------------------------------------------------

            existing_token = connection.execute(
                text("""
                    SELECT id
                    FROM oauth_tokens
                    WHERE cloud_account_id = :cloud_account_id
                    LIMIT 1
                """),
                {
                    "cloud_account_id": cloud_account_id
                }
            ).fetchone()


            if existing_token:

                token_id = existing_token[0]

                connection.execute(
                    text("""
                        UPDATE oauth_tokens
                        SET
                            access_token_encrypted = :access_token,
                            refresh_token_encrypted = COALESCE(
                                :refresh_token,
                                refresh_token_encrypted
                            ),
                            token_type = :token_type,
                            expires_at = :expires_at,
                            scope = :scope,
                            updated_at = NOW()
                        WHERE id = :id
                    """),
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_type": token_type,
                        "expires_at": expires_at,
                        "scope": scope,
                        "id": token_id,
                    }
                )

            else:

                token_id = uuid4()

                connection.execute(
                    text("""
                        INSERT INTO oauth_tokens (
                            id,
                            cloud_account_id,
                            access_token_encrypted,
                            refresh_token_encrypted,
                            token_type,
                            expires_at,
                            scope,
                            created_at,
                            updated_at
                        )
                        VALUES (
                            :id,
                            :cloud_account_id,
                            :access_token,
                            :refresh_token,
                            :token_type,
                            :expires_at,
                            :scope,
                            NOW(),
                            NOW()
                        )
                    """),
                    {
                        "id": token_id,
                        "cloud_account_id": cloud_account_id,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_type": token_type,
                        "expires_at": expires_at,
                        "scope": scope,
                    }
                )


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "Google account connected successfully",

            "user": {
                "id": str(user_id),
                "name": google_name,
                "email": google_email,
            },

            "cloud_account": {
                "id": str(cloud_account_id),
                "provider": "google_drive",
                "email": google_email,
            },

            "google": {
                "google_id": google_id,
                "email": google_email,
                "name": google_name,
            },

            "token": {
                "token_type": token_type,
                "expires_at": (
                    expires_at.isoformat()
                    if expires_at
                    else None
                ),
                "scope": scope,
                "refresh_token_received": bool(refresh_token),
            },
        }


    except SQLAlchemyError as e:

        return {
            "success": False,
            "error": "Database operation failed",
            "details": str(e),
        }


# ============================================================
# GOOGLE DRIVE TEST
# ============================================================

@app.get("/auth/google/drive-test")
def google_drive_test(
    access_token: str
):

    try:

        response = requests.get(
            GOOGLE_DRIVE_URL,
            params={
                "pageSize": 10,
                "fields": "files(id,name,mimeType,size,webViewLink)",
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            timeout=30,
        )

    except requests.RequestException as e:

        return {
            "success": False,
            "error": "Unable to connect to Google Drive",
            "details": str(e),
        }


    if not response.ok:

        return {
            "success": False,
            "error": "Google Drive request failed",
            "details": response.text,
        }


    data = response.json()

    files = data.get("files", [])


    return {
        "success": True,
        "message": "Google Drive connected successfully",
        "files_found": len(files),
        "files": files,
    }