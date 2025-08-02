## app/api/webhook.py
from fastapi import APIRouter, Request, HTTPException, status, Depends
from app.config import settings

router = APIRouter()

@router.post("/donat")
async def receive_donat(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

    token = auth.removeprefix("Bearer ").strip()
    if token != settings.API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API token")

    payload = await request.json()
    # TODO: логіка обробки донату
    return {"status": "received", "data": payload}
