
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    app_name: str = "Decision Maker AI"

    database_url: str = "sqlite:///decision_maker_ai.db"

    jwt_secret_key: str = "CHANGE_THIS_SECRET"
    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
