from pydantic import BaseModel


class AppConfig(BaseModel):
    STAGE: str = "DEVELOPMENT"
    LOG_LEVEL: int
