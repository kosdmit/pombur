from collections.abc import AsyncIterable

from dishka import Provider, provide_all, WithParents, Scope, from_context, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from apps.company_structure.application import services
from apps.company_structure.infrastructure.configs import AppConfig, PostgresConfig
from apps.company_structure.infrastructure import repository
from apps.company_structure.infrastructure import gateways
from apps.company_structure.infrastructure.connections import session_maker


class InfrastructureProvider(Provider):
    config = from_context(provides=AppConfig, scope=Scope.APP)

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
        WithParents[services.DepartmentService],  # type: ignore
    )

    repositories = provide_all(
        WithParents[repository.DepartmentRepository],  # type: ignore
    )

    gateways = provide_all(
        WithParents[gateways.DepartmentGateway],  # type: ignore
    )

