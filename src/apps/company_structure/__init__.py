from apps.company_structure import ioc
from apps.company_structure.controllers.router import router
from apps.company_structure.infrastructure.configs import AppConfig as CompanyStructureAppConfig
from apps.company_structure.infrastructure.models import Base as CompanyStructureBase

__all__ = [
    "CompanyStructureAppConfig",
    "CompanyStructureBase",
    "ioc",
    "router",
]
