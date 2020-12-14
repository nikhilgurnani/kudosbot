from pydantic import BaseSettings


class Settings(BaseSettings):
    slack_bot_token: str
    slack_signing_secret: str
    slack_client_id: str
    slack_client_secret: str
    slack_scopes: str

    class Config:
        env_file = ".env"