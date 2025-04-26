from apps.company_structure import ioc
from apps.company_structure.controllers.routers import api_router, templates_router
from apps.company_structure.infrastructure.configs import AppConfig as CompanyStructureAppConfig
from apps.company_structure.infrastructure.models import Base as CompanyStructureBase

__all__ = [
    "CompanyStructureAppConfig",
    "CompanyStructureBase",
    "api_router",
    "ioc",
    "templates_router",
]
