from pydantic import BaseModel, Field
import os


class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST')
    port: int = Field(alias='POSTGRES_PORT')
    login: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    database: str = Field(alias='POSTGRES_DB')


class AppConfig(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**os.environ))