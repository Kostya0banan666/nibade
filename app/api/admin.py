from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.deps import require_admin

router = APIRouter()

@router.get("/users")
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {"id": u.id, "username": u.username, "roblox_id": u.roblox_id, "groups": [g.name for g in u.groups]}
        for u in users
    ]

@router.get("/admin")
def admin_dashboard(user: User = Depends(require_admin)):
    return {"message": f"Welcome, admin {user.username}!"}
