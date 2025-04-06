from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from apps.company_structure.infrastructure import configs

_POSTGRES_CONNECTIONS_COUNT = 15
_POSTGRES_CONNECTIONS_OVERFLOW = 15


def session_maker(psql_config: configs.PostgresConfig) -> async_sessionmaker[AsyncSession]:
    database_uri = "postgresql+psycopg://{login}:{password}@{host}:{port}/{database}".format(  # noqa: UP032  reason: for readability
        login=psql_config.login,
        password=psql_config.password,
        host=psql_config.host,
        port=psql_config.port,
        database=psql_config.database,
    )

    engine = create_async_engine(
        database_uri,
        pool_size=_POSTGRES_CONNECTIONS_COUNT,
        max_overflow=_POSTGRES_CONNECTIONS_OVERFLOW,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
