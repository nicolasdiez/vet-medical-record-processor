import os
from dotenv import load_dotenv

# Load the environment variables from the .env.dev file
load_dotenv(".env.dev")

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

settings = Settings()