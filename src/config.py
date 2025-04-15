import os
import tomllib
from pathlib import Path

from litestar.config import allowed_hosts, compression, cors, csrf
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.template import TemplateConfig
from pydantic import BaseModel, Field

from apps import company_structure


class Config(BaseModel):
    debug: bool = Field(default_factory=lambda: os.environ.get("DEBUG") == "True")
    company_structure_app_config: company_structure.CompanyStructureAppConfig = Field(
        default_factory=company_structure.CompanyStructureAppConfig
    )


service_config = Config()
db_config = SQLAlchemyAsyncConfig(
    connection_string=service_config.company_structure_app_config.postgres.uri,
    metadata=company_structure.CompanyStructureBase.metadata,
    create_all=True,
)
cors_config = cors.CORSConfig(allow_origins=os.environ["ALLOW_ORIGINS"].split(","))
csrf_config = csrf.CSRFConfig(secret=os.environ["CSRF_SECRET"])
allowed_hosts_config = allowed_hosts.AllowedHostsConfig(
    allowed_hosts=os.environ["ALLOWED_HOSTS"].split(","),
)
compression_config = compression.CompressionConfig(backend="gzip", gzip_compress_level=9)
rate_limit_config = RateLimitConfig(rate_limit=("second", 100), exclude=["/docs"])
template_config = TemplateConfig(directory=Path("templates"), engine=JinjaTemplateEngine)

_pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
_project_metadata = tomllib.load(_pyproject_path.open("rb"))["project"]
openapi_config = OpenAPIConfig(
    title=_project_metadata["name"],
    version=_project_metadata["version"],
    render_plugins=[SwaggerRenderPlugin()],
    path="/docs",
)
