import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	DATABASE_HOSTNAME: str
	DATABASE_PASSWORD: str
	DATABASE_PORT: str
	DATABASE_NAME: str
	DATABASE_USERNAME: str
	SECRET_KEY: str
	ALGORITHM: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int


	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"

settings = Settings()

