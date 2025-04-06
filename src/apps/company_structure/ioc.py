from collections.abc import AsyncIterable

import dishka as di
from dishka import Provider, Scope, WithParents, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.company_structure.application import services
from apps.company_structure.infrastructure import gateways, repository
from apps.company_structure.infrastructure.configs import AppConfig
from apps.company_structure.infrastructure.connections import session_maker


class InfrastructureProvider(Provider):
    config = di.from_context(provides=AppConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def psql_session_maker(self, config: AppConfig) -> async_sessionmaker[AsyncSession]:
        return session_maker(psql_config=config.postgres)

    @provide(scope=Scope.REQUEST)
    async def psql_session(
        self,
        psql_session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with psql_session_maker() as session:
            yield session


class AppProvider(Provider):
    scope = Scope.REQUEST

    services = provide_all(
        WithParents[services.DepartmentService],  # type: ignore[misc]
    )

    repositories = provide_all(
        WithParents[repository.DepartmentRepository],  # type: ignore[misc]
    )

    gateways = provide_all(
        WithParents[gateways.DepartmentGateway],  # type: ignore[misc]
    )
