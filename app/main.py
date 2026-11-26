"""FastAPI application entry point for Vitoniya Edu."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, SessionLocal, engine
from app.dependencies import AuthRedirectException
from app.routers import admin, api, auth, learn, public
from app.seed import seed_initial_data

BASE_APP_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create tables and seed initial data on startup."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Vitoniya Edu API",
    description="Educational platform by Vitoniya Labs",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(BASE_APP_DIR / "static")), name="static")


@app.exception_handler(AuthRedirectException)
async def auth_redirect_handler(_: Request, __: AuthRedirectException):
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


app.include_router(public.router)
app.include_router(auth.router)
app.include_router(learn.router)
app.include_router(admin.router)
app.include_router(api.router)
