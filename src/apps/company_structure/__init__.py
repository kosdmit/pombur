from apps.company_structure import ioc
from apps.company_structure.controllers.router import router as company_structure_router
from apps.company_structure.infrastructure.configs import AppConfig as CompanyStructureAppConfig
from apps.company_structure.infrastructure.models import Base as CompanyStructureBase

__all__ = [
    "CompanyStructureAppConfig",
    "CompanyStructureBase",
    "company_structure_router",
    "ioc",
]
