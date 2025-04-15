import os

from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from pydantic import BaseModel, Field

from apps.company_structure import CompanyStructureAppConfig
from apps.company_structure.infrastructure.models import Base as CompanyStructureBase


class Config(BaseModel):
    debug: bool = Field(default_factory=lambda: os.environ.get("DEBUG") == "True")
    company_structure_app_config: CompanyStructureAppConfig = Field(
        default_factory=CompanyStructureAppConfig
    )


service_config = Config()
db_config = SQLAlchemyAsyncConfig(
    connection_string=service_config.company_structure_app_config.postgres.uri,
    metadata=CompanyStructureBase.metadata,
    create_all=True,
)
cors_config = CORSConfig(allow_origins=os.environ.get("ALLOW_ORIGINS", "").split(","))
csrf_config = CSRFConfig(secret=os.environ["CSRF_SECRET"])
