from fastapi import FastAPI
from dotenv import load_dotenv
from app.api import auth, admin, webhook
import os

load_dotenv()

app = FastAPI()

app.include_router(auth.router, prefix="")
app.include_router(admin.router, prefix="/admin")
app.include_router(webhook.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Roblox Auth App"}
