from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.config import settings
import httpx
import secrets
import urllib.parse

router = APIRouter()

AUTHORIZATION_URL = "https://apis.roblox.com/oauth/v1/authorize"
TOKEN_URL = "https://apis.roblox.com/oauth/v1/token"
USERINFO_URL = "https://apis.roblox.com/oauth/v1/userinfo"

@router.get("/login")
def login():
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": settings.ROBLOX_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.REDIRECT_URI,
        "scope": settings.ROBLOX_SCOPE,
        "state": state,
    }
    url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
def callback(code: str, state: str, db: Session = Depends(get_db)):
    data = {
        "client_id": settings.ROBLOX_CLIENT_ID,
        "client_secret": settings.ROBLOX_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    with httpx.Client() as client:
        token_resp = client.post(TOKEN_URL, data=data, headers=headers)
        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get access token")

        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        userinfo_resp = client.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
        if userinfo_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get userinfo")

        userinfo = userinfo_resp.json()
        roblox_id = userinfo.get("sub")
        username = userinfo.get("preferred_username")

        user = db.query(User).filter_by(roblox_id=roblox_id).first()
        if not user:
            user = User(roblox_id=roblox_id, username=username)
            db.add(user)
            db.commit()
            db.refresh(user)

        response = RedirectResponse(url="/")
        response.set_cookie("session_user_id", str(user.id), httponly=True)
        return response

@router.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("session_user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"id": user.id, "username": user.username, "roblox_id": user.roblox_id}
