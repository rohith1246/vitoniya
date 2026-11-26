"""FastAPI application entry point for Vitoniya Edu."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, SessionLocal, engine
from app.dependencies import AuthRedirectException, get_optional_user
from app.routers import admin, api, auth, learn, public
from app.seed import seed_initial_data
from app.templating import templates

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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    db = SessionLocal()
    try:
        user = get_optional_user(request, db)
    finally:
        db.close()

    if exc.status_code == 403:
        return templates.TemplateResponse(
            request,
            "errors/403.html",
            {"user": user, "detail": exc.detail},
            status_code=403,
        )
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request,
            "errors/404.html",
            {"user": user, "detail": exc.detail},
            status_code=404,
        )
    return templates.TemplateResponse(
        request,
        "errors/500.html",
        {"user": user, "status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )


app.include_router(public.router)
app.include_router(auth.router)
app.include_router(learn.router)
app.include_router(admin.router)
app.include_router(api.router)
