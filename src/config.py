import os

from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig
from litestar.config.allowed_hosts import AllowedHostsConfig
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.middleware.rate_limit import RateLimitConfig
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
allowed_hosts = AllowedHostsConfig(allowed_hosts=os.environ["ALLOWED_HOSTS"].split(","))
compression_config = CompressionConfig(backend="gzip", gzip_compress_level=9)
rate_limit_config = RateLimitConfig(rate_limit=("second", 1), exclude=["/docs"])
