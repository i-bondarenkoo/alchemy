from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings


class DataBaseConstructor:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def close_session(self):
        if self.engine is not None:
            return await self.engine.dispose()

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_constructor = DataBaseConstructor(
    url=settings.url,
    echo=settings.echo,
)
