"""Authentication routes: signup, login, logout."""

from typing import Optional

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_optional_user
from app.models.user import User
from app.security import create_access_token, hash_password, verify_password
from app.templating import templates

router = APIRouter(tags=["Authentication"])
settings = get_settings()


def _set_auth_cookie(response: RedirectResponse, user: User) -> None:
    token = create_access_token(user_id=user.id, role=user.role)
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/signup")
def signup_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "auth/signup.html", {"user": None, "error": None})


@router.post("/signup")
def signup_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    clean_name = full_name.strip()
    clean_email = email.strip().lower()

    if len(clean_name) < 2:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            {"user": None, "error": "Please enter your full name."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if len(password) < 6:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            {"user": None, "error": "Password must be at least 6 characters."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    existing = db.query(User).filter(User.email == clean_email).first()
    if existing:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            {"user": None, "error": "An account with this email already exists."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    new_user = User(
        full_name=clean_name,
        email=clean_email,
        password_hash=hash_password(password),
        role="student",  # Public signups are always 'student'
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    _set_auth_cookie(response, new_user)
    return response


@router.get("/login")
def login_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    if user:
        target = "/admin" if user.role == "admin" else "/dashboard"
        return RedirectResponse(url=target, status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "auth/login.html", {"user": None, "error": None})


@router.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    clean_email = email.strip().lower()
    user = db.query(User).filter(User.email == clean_email).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"user": None, "error": "Invalid email or password."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"user": None, "error": "This account has been deactivated. Contact support."},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    target = "/admin" if user.role == "admin" else "/dashboard"
    response = RedirectResponse(url=target, status_code=status.HTTP_303_SEE_OTHER)
    _set_auth_cookie(response, user)
    return response


@router.post("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key=settings.COOKIE_NAME)
    return response
