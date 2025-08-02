from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ROBLOX_CLIENT_ID: str = os.getenv("ROBLOX_CLIENT_ID", "")
    ROBLOX_CLIENT_SECRET: str = os.getenv("ROBLOX_CLIENT_SECRET", "")
    API_TOKEN: str = os.getenv("API_TOKEN", "devtoken")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")
    ROBLOX_SCOPE: str = "openid profile"

settings = Settings()
