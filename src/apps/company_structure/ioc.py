from collections.abc import AsyncIterable, AsyncIterator

import dishka as di
import litestar
from dishka import Provider, Scope, WithParents, provide, provide_all
from litestar.types.protocols import Logger
from sqlalchemy.ext.asyncio import AsyncSession

from apps.company_structure.application import services
from apps.company_structure.infrastructure import gateways, repositories


class InfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def transaction(self, request: litestar.Request) -> AsyncIterable[AsyncSession]:  # type: ignore[type-arg]  # reason: to correctly build dependencies tree
        db_session = await request.app.dependencies["db_session"](
            state=request.app.state,
            scope=request.scope,
        )
        async with db_session.begin():
            yield db_session

    @provide(scope=Scope.REQUEST)
    async def logger(self, request: litestar.Request) -> Logger:  # type: ignore[type-arg]  # reason: to correctly build dependencies tree
        return request.logger


class LitestarRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def department_repository(
        self, db_session: AsyncSession
    ) -> AsyncIterator[gateways.DepartmentGateway]:
        yield gateways.DepartmentGateway(session=db_session)

    @provide(scope=Scope.REQUEST)
    async def employee_repository(
        self, db_session: AsyncSession
    ) -> AsyncIterator[gateways.EmployeeGateway]:
        yield gateways.EmployeeGateway(session=db_session)


class AppProvider(Provider):
    scope: di.BaseScope | None = Scope.REQUEST

    services = provide_all(
        WithParents[services.DepartmentService],  # type: ignore[misc]
        WithParents[services.DepartmentTreeService],  # type: ignore[misc]
        WithParents[services.EmployeeService],  # type: ignore[misc]
    )

    repositories = provide_all(
        WithParents[repositories.department_repository.DepartmentRepository],  # type: ignore[misc]
        WithParents[repositories.department_repository.DepartmentTreeRepository],  # type: ignore[misc]
        WithParents[repositories.employee_repository.EmployeeRepository],  # type: ignore[misc]
    )
