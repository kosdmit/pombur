from collections.abc import AsyncIterable, AsyncIterator

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


class LitestarRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def department_repository(
        self, db_session: AsyncSession
    ) -> AsyncIterator[gateways.DepartmentGateway]:
        try:
            yield gateways.DepartmentGateway(session=db_session)
        except Exception:  # noqa: BLE001  # reason: catch-all
            await db_session.rollback()
        else:
            await db_session.commit()

    @provide(scope=Scope.REQUEST)
    async def employee_repository(
        self, db_session: AsyncSession
    ) -> AsyncIterator[gateways.EmployeeGateway]:
        try:
            yield gateways.EmployeeGateway(session=db_session)
        except Exception:  # noqa: BLE001  # reason: catch-all
            await db_session.rollback()
        else:
            await db_session.commit()


class AppProvider(Provider):
    scope: di.BaseScope | None = Scope.REQUEST

    services = provide_all(
        WithParents[services.DepartmentService],  # type: ignore[misc]
        WithParents[services.EmployeeService],  # type: ignore[misc]
    )

    repositories = provide_all(
        WithParents[repository.DepartmentRepository],  # type: ignore[misc]
        WithParents[repository.EmployeeRepository],  # type: ignore[misc]
    )
