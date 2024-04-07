import os
from uuid import uuid4

from sqlalchemy import Connection, create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session


class CConnection(Connection):
    def _get_unique_id(self, prefix):
        return f"__asyncpg_{prefix}_{uuid4()}__"


connect_args = {'prepared_statement_cache_size': 0,
                'statement_cache_size': 0,
                'connection_class': CConnection}

PG_USR = os.getenv('POSTGRES_USER')
PG_PWD = os.getenv('POSTGRES_PASSWORD')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_PORT = os.getenv('POSTGRES_PORT')
PG_DB_NAME = os.getenv('POSTGRES_DB')

DATABASE_ASYNC_URL = f"postgresql+asyncpg://{PG_USR}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}?prepared_statement_cache_size=0"
DB_URL = f"postgresql+psycopg2://{PG_USR}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

database = create_async_engine(DATABASE_ASYNC_URL, poolclass=NullPool, future=True, connect_args=connect_args)

async_session = sessionmaker(bind=database, class_=AsyncSession, expire_on_commit=False, autoflush=False)

sync_db = create_engine(f'postgresql://{PG_USR}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}')


def get_sync_session():
    with Session(sync_db) as session:
        return session


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
