import sys
from app.db import SessionLocal
from app.models.user import User, Group

def add_admin(roblox_id: str):
    db = SessionLocal()

    user = db.query(User).filter_by(roblox_id=roblox_id).first()
    if not user:
        print(f"User with roblox_id={roblox_id} not found.")
        sys.exit(1)

    admin_group = db.query(Group).filter_by(name="admin").first()
    if not admin_group:
        admin_group = Group(name="admin")
        db.add(admin_group)
        db.commit()
        db.refresh(admin_group)

    if admin_group not in user.groups:
        user.groups.append(admin_group)
        db.commit()
        print(f"User {user.username} added to admin group.")
    else:
        print(f"User {user.username} is already in admin group.")

    db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: poetry run python app/scripts/add_admin.py <ROBLOX_ID>")
        sys.exit(1)

    add_admin(sys.argv[1])
