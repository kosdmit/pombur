import os

from pydantic import BaseModel, Field

from apps.company_structure import CompanyStructureAppConfig


class Config(BaseModel):
    debug: bool = Field(default_factory=lambda: os.environ.get("DEBUG") == "True")
    allow_origins: list[str] = Field(
        default_factory=lambda: os.environ.get("ALLOW_ORIGINS", "*").split(","),
    )
    company_structure_app_config: CompanyStructureAppConfig = Field(
        default_factory=CompanyStructureAppConfig
    )
