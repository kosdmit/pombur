from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration

from apps.company_structure import ioc

container = make_async_container(
    ioc.InfrastructureProvider(),
    ioc.LitestarRepositoryProvider(),
    ioc.AppProvider(),
    litestar_integration.LitestarProvider(),
)
