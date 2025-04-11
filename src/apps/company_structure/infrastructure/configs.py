import os

from pydantic import BaseModel, Field


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @property
    def uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.login}:{self.password}@{self.host}:{self.port}"
            f"/{self.database}"
        )


class AppConfig(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**os.environ))
