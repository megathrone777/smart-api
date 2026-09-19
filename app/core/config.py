from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=BASE_DIR / ".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",  # allow unrelated keys in .env without breaking Settings
  )

  app_bypass_pass: str
  app_jwt_secret: str
  supabase_jwt_secret: str
  supabase_url: str
  supabase_publishable_key: str
  supabase_service_role_key: str

settings = Settings()