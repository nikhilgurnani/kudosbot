from pydantic import BaseSettings


class Settings(BaseSettings):
    slack_auth_token: str
    slack_token: str

    class Config:
        env_file = ".env"