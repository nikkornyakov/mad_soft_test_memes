from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import DEFAULT_PAGE, DEFAULT_LIMIT_PER_PAGE
from models import Meme


class CRUDBase:
    """Базовый класс для операций CRUD."""

    def __init__(self, model):
        """
        Метод инициализации класса.
        Принимает модель в качестве параметра.
        """
        self.model = model

    async def create(self, data, session: AsyncSession):
        """Метод для создания мема."""
        object = self.model(**data.dict())
        session.add(object)
        await session.commit()
        await session.refresh(object)
        return object

    async def update(self, object, new_data, session: AsyncSession):
        """Метод для изменения мема."""
        update_data = new_data.model_dump()
        for field in jsonable_encoder(object):
            if field in update_data:
                setattr(object, field, update_data[field])
        session.add(object)
        await session.commit()
        await session.refresh(object)
        return object

    async def remove(self, object, session: AsyncSession):
        """Метод для удаления мема."""
        await session.delete(object)
        await session.commit()
        return object

    async def get(self, object_id: int, session: AsyncSession):
        """Метод для получения объекта по id."""
        return (
            (
                await session.execute(
                    select(self.model).where(self.model.id == object_id)
                )
            )
            .scalars()
            .first()
        )

    async def get_all(self, session: AsyncSession):
        """Метод для получения всех мемов."""
        return (
            (await session.execute(select(self.model).order_by(self.model.id)))
            .scalars()
            .all()
        )

    async def get_all_with_pagination(
        self, page: int, limit: int, session: AsyncSession
    ):
        """Метод для получения всех мемов с пагинацией."""
        limit = limit or DEFAULT_LIMIT_PER_PAGE
        offset_for_page = page - DEFAULT_PAGE
        return (
            (
                await session.execute(
                    select(self.model)
                    .offset(
                        offset_for_page
                        if page <= DEFAULT_PAGE
                        else offset_for_page * limit
                    )
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )


memes_crud = CRUDBase(Meme)
